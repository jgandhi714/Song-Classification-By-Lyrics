# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 21:05:08 2016

@author: Javesh
"""
import BagOfWords as BOW
from collections import Counter
import os
import scipy
import matplotlib.pyplot as plt
import pandas as pd

class ArtistVocabulary:
    def __init__(self, directory, artist = 'unspecified'):
        self.artist = artist        
        self.directory = directory
        self.num_docs = len(os.listdir(directory))
        self.stop_words = ['verse', 'produced', '2x', 'you', 'i', 'the', 'me', 'to', 'it', 'my', 'for', 'a', 'your', 'and', 'chorus', 'on', 'in', 'that', 'im', 'so']
        self.vocabulary = self.create_vocabulary()
        self.number_of_unique_words = len(self.vocabulary)
        self.total_words = self.count_total_words()
        self.words = self.vocabulary.keys()
        self.word_df = self.create_word_df()
        
    def create_vocabulary(self):
        vocabulary = Counter()
        for file in os.listdir(self.directory):
            file_path = self.directory + "/" + file            
            temp_bag = BOW.BagOfWords(file_path)
            vocabulary += temp_bag.create_bag_of_words()
        return vocabulary
    
    def sort_vocabulary(self):
        vocabulary = self.create_vocabulary()
        sorted_vocabulary = vocabulary.most_common()
        return sorted_vocabulary
    
    def plot_vocabulary(self, end_num = 20):
        sorted_vocabulary = self.sort_vocabulary()
        
        x = []
        y = []
        
        for value in sorted_vocabulary[0:end_num]:
            x.append(value[0])
            y.append(value[0])
        
        index = scipy.arange(end_num)
        
        f = plt.figure()
        ax = f.add_axes([0.1, 0.1, 1.5, 1.0])
        ax.bar(index, y, align = 'center')
        ax.set_xticks(index)
        ax.set_labels(x)
        f.show()
    
    def get_word_freq(self, word):
        word = word.lower()
        if word in self.vocabulary:
            return self.vocabulary[word]
        else:
            return 0
    
    def count_total_words(self):
        total = 0
        for word, freq in self.vocabulary.items():
            total += freq
        return total
    
    def get_word_probability(self, word):
        if word in self.vocabulary:
            word_frequency = self.get_word_freq(word)
            total_words = self.total_words
            probability = float(word_frequency)/float(total_words)
            return probability
        else:
            return 0
    
    def create_word_df(self):
        word_list = []
        frequency = []
        probability = []
        
        for word in self.words:
            word_list.append(word)
            frequency.append(self.vocabulary[word])
            probability.append(self.get_word_probability(word))
        
        word_df = pd.DataFrame({'Word':word_list, 'Frequency': frequency, 'Probability': probability})
        word_df = word_df.set_index('Word')
        return word_df
    

        