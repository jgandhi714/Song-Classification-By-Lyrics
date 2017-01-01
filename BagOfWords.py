# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 19:20:31 2016

@author: Javesh
"""
import re
import string
from collections import Counter
import scipy
import matplotlib.pyplot as plt
import pandas as pd

class BagOfWords:
    def __init__(self, file_path):
        self.path = file_path
        self.stop_words = ['verse', 'produced', '2x', 'you', 'i', 'the', 'me', 'to', 'it', 'my', 'for', 'a', 'your', 'and', 'chorus', 'on', 'in', 'that', 'im', 'so']
        self.bag_of_words = self.create_bag_of_words()  
        self.number_of_unique_words = len(self.bag_of_words)
        self.total_words = self.count_total_words()
        self.words = self.bag_of_words.keys()
        self.word_df = self.create_word_df()
        
        
    def create_bag_of_words(self):
        stop_words = self.stop_words        
        path = self.path
        words = open(path).read()
        words = re.sub("\[[^]]*\]", '', words)
        words = words.split()
        #lower case each word            
        for i in range(len(words)):
            words[i] = words[i].lower()
        #get rid of punctuation
        words = [''.join(char for char in word  if char not in string.punctuation) for word in words]
        #take out stop words
        words = [word for word in words if word not in stop_words]
        #take out numbers
        words = [word for word in words if (word.isdigit() == False)]
        bag_of_words = Counter(words)
        if '' in bag_of_words:
            del bag_of_words['']
        return bag_of_words
    
    def sort_bag_of_words(self):
        bag_of_words = self.bag_of_words
        sorted_bag_of_words = bag_of_words.most_common()
        return sorted_bag_of_words
    
    def plot_bag_of_words(self, end_num = 20):
        sorted_bag_of_words = self.sort_bag_of_words()
        
        x = []
        y = []
        
        for value in sorted_bag_of_words[0:end_num]:
            x.append(value[0])
            y.append(value[1])
        
        index = scipy.arange(end_num)
        
        f = plt.figure()
        ax = f.add_axes([0.1, 0.1, 1.5, 1.0])
        ax.bar(index, y, align='center')
        ax.set_xticks(index)
        ax.set_xticklabels(x)
        f.suptitle(" Word Frequency in " + self.path)
        f.show()
    
    def get_word_freq(self, word):
        word = word.lower()
        if word in self.bag_of_words:
            return self.bag_of_words[word]
        else:
            return 0
    
    def count_total_words(self):
        total = 0
        for word, freq in self.bag_of_words.items():
            total += freq
        return total
    
    def get_word_probability(self, word):
        if word in self.bag_of_words:
            word_frequency = self.get_word_freq(word)
            total_words = self.total_words
            probability = float(word_frequency)/float(total_words)
            return probability
        else:
            return 0
    
    def create_word_df(self):
        word_list= []
        frequency = []
        probability = []
        
        for word in self.words:
            word_list.append(word)
            frequency.append(self.bag_of_words[word])
            probability.append(self.get_word_probability(word))
        
        word_df = pd.DataFrame({'Word':word_list, 'Frequency': frequency, 'Probability': probability})
        return word_df
    
    