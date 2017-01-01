# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:57:31 2016

@author: Javesh
"""
#import Cleaned_Scraper
import os
import shutil
import math
import random


class Random_Subsets:
    def __init__(self, scraper):
        self.scraper = scraper
        self.artist = self.scraper.artist
        self.albums = self.scraper.albums
        
        self.create_random_directories() 
        
        self.training_directory = scraper.artist_directory + "/random/training"
        self.test_directory = scraper.artist_directory + "/random/test"
        self.amt_training_docs = len(os.listdir(self.training_directory))
        self.amt_test_docs = len(os.listdir(self.test_directory))

    def create_random_directories(self, training_data_size = 0):
        random_training_directory = self.scraper.artist_directory + '/random/training'
        random_test_directory = self.scraper.artist_directory + '/random/test'        
        if not os.path.exists(random_training_directory) and not os.path.exists(random_test_directory):
            os.makedirs(random_training_directory)
            os.makedirs(random_test_directory)
        else:
            for file in os.listdir(random_training_directory):
                os.remove(random_training_directory + '/' + file)
            for file in os.listdir(random_test_directory):
                os.remove(random_test_directory + '/' + file)
        
        training_set = set()
        test_set = set()
        
        if training_data_size == 0:
            directory_length = len(os.listdir(self.scraper.clean_directory))            
            training_data_size = math.ceil(0.6 * directory_length)
            
        while training_set == None or len(training_set) < training_data_size:
            chosen_file = random.choice(os.listdir(self.scraper.clean_directory))
            #chosen_path = scraper.clean_directory + '/' + chosen_file
            training_set.add(chosen_file)
        for file in training_set:
            shutil.copy(self.scraper.clean_directory + '/' + file, random_training_directory + '/' + file)
        for file in os.listdir(self.scraper.clean_directory):
            if file not in training_set:
                test_set.add(file)
        for file in test_set:
            shutil.copy(self.scraper.clean_directory + '/' + file, random_test_directory + '/' + file)
        
        print("training set:{}, test set:{}".format(training_set, test_set))
            