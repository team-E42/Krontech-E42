from trainenv import *

import torch
import torch.nn as nn
import torch.optim as optim

# parameters
tuple_size = 5
value_vocab_size = 4096
embed_size = 256
hidden_size = 256
batch_size = 32
max_length = 3

def collate_fn(batch):
    inputs, targets = zip(*batch)

    input_lengths = [x.size(0) for x in inputs]
    target_lengths = [y.size(0) for y in targets]

    max_input_len = max(input_lengths)
    max_target_len = max(target_lengths)

    padded_inputs = []
    padded_targets = []

    for x in inputs:
        pad_len = max_input_len - x.size(0)

        if pad_len > 0:
            pad = torch.zeros(pad_len, tuple_size, dtype=torch.long)
            x = torch.cat([x, pad], dim=0)

        padded_inputs.append(x)

    for y in targets:
        pad_len = max_target_len - y.size(0)
        if pad_len > 0:
            pad = torch.full((pad_len,), PAD_TOKEN, dtype=torch.long)
            y = torch.cat([y, pad])

        padded_targets.append(y)

    return torch.stack(padded_inputs).to(device), torch.stack(padded_targets).to(device)

loader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)

class TupleEmbedding(nn.Module):
    def __init__(self, value_vocab_size, embedding_dim, tuple_size=5):
        super().__init__()
        self.embeddings = nn.ModuleList([
            nn.Embedding(
                value_vocab_size,
                embedding_dim
            )
            for _ in range(tuple_size)
        ])

        self.projection = nn.Linear(embedding_dim * tuple_size, embedding_dim)

    def forward(self, x):
        parts = []
        for i in range(tuple_size):
            emb = self.embeddings[i](x[:, :, i])
            parts.append(emb)

        x = torch.cat(parts, dim=-1)
        x = self.projection(x)
        return x


class Encoder(nn.Module):
    def __init__(self, value_vocab_size, embedding_dim, hidden_size):
        super().__init__()
        self.hidden_size = hidden_size
        self.embedding = TupleEmbedding(value_vocab_size, embedding_dim)
        self.gru = nn.GRU(embedding_dim, hidden_size, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, hidden = self.gru(embedded)
        return outputs, hidden

class AttentionDecoder(nn.Module):
    def __init__(self, hidden_size, output_size):
        super().__init__()
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.attn = nn.MultiheadAttention(hidden_size, num_heads=1, batch_first=True)
        self.gru = nn.GRU(hidden_size * 2, hidden_size, batch_first=True)
        self.out = nn.Linear(hidden_size, output_size)

    def forward(self, encoder_outputs, encoder_hidden, target_tensor=None, max_lenghts=32):
        batch_size = encoder_outputs.size(0)

        decoder_input = torch.full((batch_size, 1), SOS_TOKEN, device=device, dtype=torch.long)
        decoder_hidden = encoder_hidden
        outputs = []
        for i in range(max_lenghts):
            embedded = self.embedding(decoder_input)
            query = decoder_hidden.permute(1,0,2)
            context, _ = self.attn(
                query,
                encoder_outputs,
                encoder_outputs
            )

            gru_input = torch.cat([embedded, context], dim=2)
            output, decoder_hidden = self.gru(gru_input, decoder_hidden)
            logits = self.out(output)
            outputs.append(logits)
            if target_tensor is not None:
                decoder_input = target_tensor[:, i].unsqueeze(1)
            else:
                decoder_input = logits.argmax(-1)

        outputs = torch.cat(outputs, dim=1)
        return outputs

if __name__ == "__main__":
    encoder = Encoder(value_vocab_size, embed_size, hidden_size).to(device)
    decoder = AttentionDecoder(hidden_size, chvb.char_count).to(device)

    encoder_optimizer = torch.optim.Adam(encoder.parameters(), lr=0.001)
    decoder_optimizer = torch.optim.Adam(decoder.parameters(), lr=0.001)

    criterion = nn.CrossEntropyLoss(ignore_index=PAD_TOKEN)
    epochs = 50
    for epoch in range(epochs):
        total_loss = 0
        for input_tensor, target_tensor in loader:
            encoder_optimizer.zero_grad()
            decoder_optimizer.zero_grad()

            encoder_outputs, encoder_hidden = encoder(input_tensor)
            decoder_outputs = decoder(encoder_outputs, encoder_hidden, target_tensor, max_lenghts=max_length)

            loss = criterion(
                decoder_outputs.view(-1, chvb.char_count),
                target_tensor.view(-1)
            )

            loss.backward()
            encoder_optimizer.step()
            decoder_optimizer.step()

            total_loss += loss.item()

        print(
            f"Epoch {epoch+1} Loss: "
            f"{total_loss / len(loader):.4f}"
        )

        checkpoint = {
            "encoder_state_dict": encoder.state_dict(),
            "decoder_state_dict": decoder.state_dict(),
            "encoder_optimizer_state_dict": encoder_optimizer.state_dict(),
            "decoder_optimizer_state_dict": decoder_optimizer.state_dict(),
            "output_vocab": chvb.__dict__,
            "hidden_size": hidden_size
        }

        torch.save(checkpoint, s2e_model_path)

