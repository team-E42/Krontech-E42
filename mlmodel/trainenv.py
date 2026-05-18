import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from gensim.models import KeyedVectors
from torch.utils.data import Dataset, DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}.")

SOS_TOKEN = 0
EOS_TOKEN = 1
PAD_TOKEN = 2
class Vocabulary: 
    def __init__(self):
        self.index2char = {
            SOS_TOKEN: "<SOS>",
            EOS_TOKEN: "<EOS>",
            PAD_TOKEN: "<PAD>"
        }

        self.char2index = {
            "<SOS>": SOS_TOKEN,
            "<EOS>": EOS_TOKEN,
            "<PAD>": PAD_TOKEN
        }

        self.char_count = 3

    def add_letter(self, letter):
        if letter not in self.char2index:
            self.char2index[letter] = self.char_count
            self.index2char[self.char_count] = letter
            self.char_count += 1
            
    def add_word(self, word):
        for letter in word:
            self.add_letter(letter)

training_data = "./data/train.txt"
s2e_model_path = "./pretrained/s2e_model.pt"

chvb = Vocabulary()

print("Loading data...")
file = open(training_data, "r")
data = [([([int(x) for x in line.split(" ")[0:5]])], line.split(" ")[5]) for line in file.read().splitlines()]

for dp in data:
    chvb.add_letter(dp[1])

class TranslationDataset(Dataset):
    def __init__(self, pairs):
        self.pairs = pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        pair = self.pairs[idx]

        inp = torch.tensor(pair[0], dtype=torch.long)
        tgt = [SOS_TOKEN] + [chvb.char2index[c] for c in pair[1]] + [EOS_TOKEN]
        tgt = torch.tensor(tgt, dtype=torch.long)
        return inp, tgt

random.shuffle(data)
dataset = TranslationDataset(data)
