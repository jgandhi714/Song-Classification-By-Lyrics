# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 11:13:16 2016

@author: Javesh
"""

import Genius_Scraper as GS
import Cleaned_Scraper as CS
import Random_Subsets as RS
import BagOfWords as BOW
import ArtistVocabulary as AS
import NB_Classifier as NB

import os
import random
import shutil




#import matplotlib.pyplot as plt


if __name__ == "__main__":
    Drake = CS.Cleaned_Scraper('Drake', ['Thank Me Later', 'Take Care', 'Nothing Was the Same', 'Views', 'Room For Improvement', 'Comeback Season', 'So Far Gone', 'If You"'"re Reading This It"'"s Too Late', 'What a Time to Be Alive'])  
    Drake_subset = RS.Random_Subsets(Drake)
    Drake_vocab = AS.ArtistVocabulary(Drake_subset.training_directory, 'Drake')
    
    JL = CS.Cleaned_Scraper("John Legend", ['Get Lifted', 'Once Again', 'Evolver', 'Love in the Future', 'Darkness and Light'])
    JL_subset = RS.Random_Subsets(JL)
    JL_vocab = AS.ArtistVocabulary(JL_subset.training_directory, 'John Legend')
    
    results = []
    random_list = []
    for file in os.listdir(Drake_subset.test_directory):
        path = Drake_subset.test_directory + '/' + file
        bag = BOW.BagOfWords(path)        
        classifier = NB.NB_Classifier([Drake_vocab, JL_vocab], bag)
        results.append(classifier.classify())
        random_list.append(random.choice(['Drake', 'John Legend']))
    print(results)
    
    correct = 0
    correct_random = 0
    for result in results:
        if result == 'Drake':
            correct+=1
    for random_result in random_list:
        if random_result == 'Drake':
            correct_random += 1
    
    accuracy = float(correct)/float(len(results))
    print (accuracy)
    
    random_accuracy = float(correct_random)/float(len(results))
    print (random_accuracy)
    
    results = []
    random_list = []
    for file in os.listdir(JL_subset.test_directory):
        path = JL_subset.test_directory + '/' + file
        bag = BOW.BagOfWords(path)        
        classifier = NB.NB_Classifier([Drake_vocab, JL_vocab], bag)
        results.append(classifier.classify())
        random_list.append(random.choice(['Drake', 'John Legend']))
    print(results)
    
    correct = 0
    correct_random = 0
    for result in results:
        if result == 'John Legend':
            correct+=1
    for random_result in random_list:
        if random_result == 'John Legend':
            correct_random += 1
    
    accuracy = float(correct)/float(len(results))
    print (accuracy)
    
    random_accuracy = float(correct_random)/float(len(results))
    print (random_accuracy)
        
        

  
#==============================================================================
#     Chance = GS.Genius_Scraper('Chance The Rapper', ['10 Day', 'Acid Rap', 'Coloring Book'])
# 
#     Drake = GS.Genius_Scraper('Drake', ['Thank Me Later', 'Take Care', 'Nothing Was the Same', 'Views', 'Room For Improvement', 'Comeback Season', 'So Far Gone', 'If You"'"re Reading This It"'"s Too Late', 'What a Time to Be Alive'])    
#     #Drake.create_txt()
# #==============================================================================
# #     Drake.create_new_directory()
# #     Drake.remove_extras()
# #     Drake.iso_artist_lyrics()
# #==============================================================================
#     Drake.master_clean()    
#     Drake.word_count_plot()    
#     
#     
#     Pharrell = GS.Genius_Scraper("Pharrell Williams", ['In My Mind', 'G I R L'])
#     
#     Bruno_Mars = GS.Genius_Scraper("Bruno Mars", ['Doo-Wops & Hooligans', 'Unorthodox Jukebox', '24K Magic'])
#     John_Legend = GS.Genius_Scraper("John Legend", ['Get Lifted', 'Once Again', 'Evolver', 'Love in the Future', 'Darkness and Light'])
#==============================================================================
    
#==============================================================================
#     Lil_Yachty = GS.Genius_Scraper("Lil Yachty", ['Lil Boat The Mixtape', 'Summer Songs 2', 'Summer Songs EP'])
#     bag = BOW.BagOfWords(Lil_Yachty)
#     word_df = bag.word_df
#     
#==============================================================================
    
    
#==============================================================================
#         
#     Jeremih = CS.Cleaned_Scraper('Jeremih', ['Jeremih', 'All About You', 'Late Nights'], True)
#     Jeremih_RS = RS.Random_Subsets(Jeremih)
#                 
#     directory = Jeremih_RS.training_directory            
#     JeremihVocabulary = AV.ArtistVocabulary('Jeremih', directory)
#==============================================================================
    
    
    
    