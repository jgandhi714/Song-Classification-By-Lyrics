# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:42:13 2016

@author: Javesh
"""

import Genius_Scraper as GS
from collections import Counter
import os
import re
import string
import scipy
import matplotlib.pyplot as plt

class BagOfWords:
    
    def __init__(self, scraper, data_set = 'total'):
        self.scraper = scraper
        self.stop_words = ['verse', 'produced', '2x', 'you', 'i', 'the', 'me', 'to', 'it', 'my', 'for', 'a', 'your', 'and', 'chorus', 'on', 'in', 'that', 'im', 'so']

        if data_set == 'total':
            self.directory = scraper.clean_directory
            #self.total_bag_of_words = self.bag_of_words(self.directory)
        elif data_set == 'training':
            self.directory = scraper.training_directory
            #self.training_bag_of_words = self.bag_of_words(directory = self.training_directory)
        elif data_set == 'test':
            self.directory = scraper.test_directory
            #self.test_bag_of_words = self.bag_of_words(directory = self.test_directory)
        else:
            print ("bad data_set param, will default to clean_directory")
            self.directory = scraper.clean_directory
        
        self.bag_of_words = self.bag_of_words()
        self.number_of_unique_words = len(self.bag_of_words)   
        self.total_words = self.count_total_words()
        self.words = self.bag_of_words.keys()
        
    def bag_of_words(self):
        """
        Perform after the files have been compiled and cleaned via create_txt and master_clean
        """   
        directory = self.directory
        #list of stop words (words that appear to be insignificant and should not be included for training the algorithm)        
        stop_words = self.stop_words
        
        bag_of_words = Counter()
        #clean_directory = self.clean_directory
        for file in os.listdir(directory):
            file_path = directory + "/" + file
            words = open(file_path).read()
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
            bag_of_words += Counter(words) 
        if '' in bag_of_words:
            del bag_of_words['']
       
        return bag_of_words
    
    def sort_bag_of_words(self, directory = None):
        bag_of_words = self.bag_of_words(directory)
        bag_of_words_sorted = bag_of_words.most_common()
        return bag_of_words_sorted
    
    def bag_of_words_plot(self, directory = None, end_num = 20):
        bag_of_words_sorted = self.sort_bag_of_words(directory)
        albums_for_title = self.albums[0]
        for i in range(1, len(self.albums) - 1):
            albums_for_title += ", " + self.albums[i]
        albums_for_title += ", and " + self.albums[-1]
            
        
        x = []
        y=[] 
        
        for value in bag_of_words_sorted[0:end_num]:
            x.append(value[0])
            y.append(value[1])
        
        test_index = scipy.arange(end_num)
        #y = scipy.array([4,7,6,5])
        #plt.title(self.artist + " Word Frequency in " + albums_for_title)        
        f = plt.figure()
        ax = f.add_axes([0.1, 0.1, 1.5, 1.0])
        ax.bar(test_index, y, align='center')
        ax.set_xticks(test_index)
        ax.set_xticklabels(x)
        f.suptitle(self.artist + " Word Frequency in " + albums_for_title)
        f.show()
    
    def word_freq(self, word):
        if word in self.bag_of_words:
            return self.bag_of_words[word]
        else:
            return 0    
            
    def count_total_words(self):
        total = 0        
        for word, freq in self.bag_of_words.items():
            total+= freq
        return total
        
    def word_probability(self, word):
        if word in self.bag_of_words:
            word_frequency = self.word_freq(self, word)
            total_words = self.total_words
            probability = word_frequency / total_words
            return probability
        else:
            return 0
