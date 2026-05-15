from trainenv import *

import random
import torch
import torch.nn as nn
import torch.optim as optim


examples = []
random.shuffle(examples)

class TranslationDataset(Dataset):
    def __innit__(self, examples):
        self.examples = examples
    def __len__(self):
        return len(self.examples)
    def __getitem__(self, idx):
        input_sequence, target_sequence = self.examples[idx]
        input_tokens = [
            vocabulary.word2index.get(word, vocabulary.word2index["<UNK>"])
            for word in input_sequence.split()
        ]
        target_tokens = [
            vocabulary.word2index.get(word, vocabulary.word2index["<UNK>"])
            for word in target_sequence.split()
        ]
        target_tokens.append(EOS_TOKEN)
        return(torch.tensor(input_tokens, dtype=torch.long),
               torch.tensor(target_tokens, dtype=torch.long))

dataset = TranslationDataset(examples)

def collate_fn(batch):
    inputs, targets = zip(*batch)
    
    input_lenghts = [len(seq) for seq in inputs]
    target_lenghts = [len(seq) for seq in targets]

    padded_inputs = nn.utils.rnn.pad_sequence(inputs, batch_first=True)
    padded_targets = nn.utils.rnn.pad_sequence(targets, batch_first=True)

    return padded_inputs, padded_targets, input_lenghts, target_lenghts

loader = DataLoader(dataset, batch_size=16, shuffle=True, collate_fn=collate_fn)


class Encoder(nn.Module):
    def __init__(self, input_vocabulary_length, hidden_size):
        super().__init__()
        self.embedding = nn.Embedding(input_vocabulary_length, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        outputs, hidden = self.gru(embedded)
        return outputs, hidden

class Attention(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.attn = nn.Linear(hidden_size * 2, hidden_size)
        self.v = nn.Linear(hidden_size, 1)

    def forward(self, hidden, encoder_outputs):
        batch_size = encoder_outputs.size(0)
        seq_len = encoder_outputs.size(1)

        hidden = hidden[-1]
        hidden = hidden.unsqueeze(1).repeat(1, seq_len, 1)
        energy = torch.tanh(self.attn(
            torch.cat((hidden, encoder_outputs), dim=2)
        ))

        attention = self.v(energy).squeeze(2)
        return torch.softmax(attention, dim=1)

class AttentionDecoder(nn.Module):
    def __init__(self, hidden_size, output_vocabulary_size, embedding_matrix, embed_dim):
        super().__init__()
        self.embedding = nn.Embedding.from_pretrained(embedding_matrix, freeze=False)
        self.attention = Attention(hidden_size)
        self.gru = nn.GRU(embed_dim + hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_vocabulary_size)

    def forward(self, input_token, hidden, encoder_outputs):
        embed = self.embedding(input_token)
        attention_weights = self.attention(hidden, encoder_outputs)
        context = torch.bmm(attention_weights.unsqueeze(1), encoder_outputs)
        gru_input = torch.cat((embed, context), dim=2)
        output, hidden = self.gru(gru_input, hidden)
        prediction = self.fc(output)
        return prediction, hidden


# parameters
INPUT_VOCABULARY_SIZE = 2
HIDDEN_SIZE = 128
EMBED_DIM = 2
vocabulary = Vocabulary()

embedding_matrix = np.random.normal(
    scale=0.6,
    size=(vocabulary.n_words, EMBED_DIM)
)

for word, idx in vocabulary.word2index.items():
    if word in vocabulary.word2vec:
        embedding_matrix[idx] = vocabulary.word2vec[word][:EMBED_DIM]

embedding_matrix = torch.FloatTensor(embedding_matrix)

encoder = Encoder(INPUT_VOCABULARY_SIZE, HIDDEN_SIZE).to(device)
decoder = AttentionDecoder(HIDDEN_SIZE, vocabulary.word_count, embedding_matrix)

