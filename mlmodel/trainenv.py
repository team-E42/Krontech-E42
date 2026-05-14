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
class Vocabulary: 
    def __init__(self):
        self.index2word = {
            SOS_TOKEN: "<SOS>",
            EOS_TOKEN: "<EOS>"
        }

        self.word2index = {
            "<SOS>": SOS_TOKEN,
            "<EOS>": EOS_TOKEN
        }

        self.word_count = 2

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.word_count
            self.index2word[self.word_count] = word
            self.word_count += 1
            
    def add_sentance(self, sentance):
        for word in sentance.split():
            self.add_word(word)

s2e_model_path = "./pretrained/s2e_model.pt"
word2vec_model_path = "./pretrained/word2vec_model.bin"

word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
print("Loaded word2vec successfully.")

