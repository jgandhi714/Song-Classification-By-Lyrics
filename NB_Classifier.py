# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 22:25:22 2016

@author: Javesh
"""
import pandas as pd
from collections import Counter
import math

class NB_Classifier:
    def __init__(self, list_of_vocab, bag_of_words):
        self.list_of_vocab = list_of_vocab
        self.bag_of_words = bag_of_words
        self.classify()
    
    def get_total_training_docs(self):
        total_files = 0
        for vocab in self.list_of_vocab:
            total_files+=vocab.num_docs
        return total_files
    
    def calculate_prior_probabilities(self):
        artists = []
        prior_probs = []        
        total_files = self.get_total_training_docs()
        for vocab in self.list_of_vocab:
            artists.append(vocab.artist)
            prior_prob = float(vocab.num_docs)/float(total_files)
            prior_probs.append(prior_prob)
        prior_probs_df = pd.DataFrame({'Artist': artists, 'Prior Probability': prior_probs})
        prior_probs_df = prior_probs_df.set_index('Artist')
        return prior_probs_df
    
    def combine_vocab(self):
        combined_vocabulary = Counter()
        for vocab in self.list_of_vocab:
            combined_vocabulary+=vocab.vocabulary
        return combined_vocabulary 
    
    def create_blank_score_df(self):
        artists = []     
        scores = []
        for vocab in self.list_of_vocab:
            artists.append(vocab.artist)
            scores.append(0)
        score_df = pd.DataFrame({'Artist':artists, 'Score': scores})
        score_df = score_df.set_index('Artist')
        return score_df
    
    def calculate_scores(self):
        score_df = self.create_blank_score_df()        
        prior_probs_df = self.calculate_prior_probabilities()
        bag_of_words = self.bag_of_words
        combined_vocab = self.combine_vocab()
        for word, count in bag_of_words.bag_of_words.items():
            if not word in combined_vocab.keys():
                continue
            p_word = combined_vocab[word]/sum(combined_vocab.values())
            for vocab in self.list_of_vocab:
                artist = vocab.artist
                try:
                    p_word_given_artist = vocab.word_df.get_value(word, 'Probability')
                except:
                    p_word_given_artist = 0
                if p_word_given_artist > 0:
                    add_to_score = math.log(float(count) * p_word_given_artist/p_word)
                    current_score = score_df.get_value(artist, 'Score')
                    score_df.set_value(artist, 'Score', current_score + add_to_score)
        for vocab in self.list_of_vocab:
            current_value = score_df.get_value(vocab.artist, 'Score')
            prior_probability = prior_probs_df.get_value(vocab.artist, 'Prior Probability')
            score_df.set_value(vocab.artist, 'Score', math.exp(current_value + math.log(prior_probability)))
        return score_df
    
    def classify(self):
        score_df = self.calculate_scores()
        score_df = score_df.sort('Score',  ascending = False)
        return score_df.index.values[0]
    
        
            
    
                    
                    
                    
                
        
        
    
    
        
        