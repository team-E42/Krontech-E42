from trainenv import *
from train import *

checkpoint = torch.load(
    s2e_model_path,
    map_location=device
)

output_vocab = Vocabulary()
output_vocab.__dict__ = checkpoint[
    "output_vocab"
]

encoder = Encoder(value_vocab_size, embed_size, hidden_size).to(device)
decoder = AttentionDecoder(hidden_size, output_vocab.char_count).to(device)
encoder.load_state_dict(checkpoint["encoder_state_dict"])
decoder.load_state_dict(checkpoint["decoder_state_dict"])

encoder.eval()
decoder.eval()

print("Model loaded successfully")

def predict(sequence, max_length=max_length):
    sequence = [sequence]
    with torch.no_grad():
        inp = torch.tensor([sequence], dtype=torch.long, device=device)
        encoder_outputs, encoder_hidden = encoder(inp)

        outputs = decoder(encoder_outputs, encoder_hidden, target_tensor=None)
        pred_ids = outputs.argmax(-1).squeeze()
        chars = []
        for idx in pred_ids:
            idx = idx.item()
            if idx == EOS_TOKEN:
                break

            chars.append(output_vocab.index2char[idx])

        return "".join(chars)