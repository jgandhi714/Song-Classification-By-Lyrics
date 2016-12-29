# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 11:13:16 2016

@author: Javesh
"""

import Genius_Scraper as GS
from collections import Counter
import os
import string

if __name__ == "__main__":
  
    Chance = GS.Genius_Scraper('Chance The Rapper', ['10 Day', 'Acid Rap', 'Coloring Book'])
#==============================================================================
#     Chance.create_txt()
#     Chance.master_clean()
#==============================================================================
    
    Pharrell = GS.Genius_Scraper("Pharrell Williams", ['In My Mind', 'G I R L'])
#==============================================================================
#     Pharrell.create_txt()
#     Pharrell.master_clean()
#==============================================================================
    
    Bruno_Mars = GS.Genius_Scraper("Bruno Mars", ['Doo-Wops & Hooligans', 'Unorthodox Jukebox', '24K Magic'])
#==============================================================================
#     Bruno_Mars.create_txt()
#     Bruno_Mars.master_clean()
#     
#==============================================================================
    
    artist_list = [Chance, Pharrell, Bruno_Mars]
    word_count_dict = {}
    
    for artist in artist_list:
        artist_split = artist.artist.split()        
        remove_list = ['verse', 'produced', '2x', 'you', 'i', 'the', 'me', 'to', 'it', 'my', 'for', 'a', 'and', 'chorus']
        for element in artist_split:
            remove_list.append(element)
        word_count = Counter()
        clean_directory = artist.clean_directory
        for file in os.listdir(clean_directory):
            file_path = clean_directory + "/" + file
            words = open(file_path).read()
            words = words.split()
            for i in range(len(words)):
                words[i] = words[i].lower()
            #words = [word for word in words if (word.isdigit() == False)] 
            words = [''.join(char for char in word  if char not in string.punctuation) for word in words]
            words = [word for word in words if word not in remove_list]
            words = [word for word in words if (word.isdigit() == False)]
            word_count += Counter(words) 
        word_count = word_count.most_common()
        word_count_dict[artist.artist] = word_count
    
    
    
    
    
    
    