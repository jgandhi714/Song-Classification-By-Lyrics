# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 15:49:38 2016

@author: Javesh
"""

import Genius_Scraper as GS
import os
import shutil
from difflib import SequenceMatcher as sm

def master_function(scraper):
    remove_extras(scraper)
    iso_artist_lyrics(scraper)


def create_new_directory(scraper):
    #creates new directory called clean and copies every lyric file
    clean_directory = scraper.artist_directory + '/clean'    
    if not os.path.exists(clean_directory):
        os.makedirs(clean_directory)
        for lyric in os.listdir(scraper.lyrics_directory):
            if os.path.isfile(scraper.lyrics_directory + '/' + lyric):
                shutil.copy(scraper.lyrics_directory + '/' + lyric, clean_directory + '/' + lyric)

def remove_extras(scraper):
    #removes files like tracklist and remix files scraped from Genius
    create_new_directory(scraper)    
    removal_list = []    
    if not os.path.exists(scraper.artist_directory + '/tracklist_album_art'):
        os.makedirs(scraper.artist_directory + '/tracklist_album_art')
    
    if not os.path.exists(scraper.artist_directory + '/remix'):
        os.makedirs(scraper.artist_directory + '/remix')
    
    if not os.path.exists(scraper.artist_directory + '/small'):
        os.makedirs(scraper.artist_directory + '/small')
        
    clean_directory = scraper.artist_directory + '/clean'    
    
    for lyric in os.listdir(clean_directory):
        lyric_path = clean_directory + '/' + lyric        
        if "tracklist" in lyric.lower() or "album art" in lyric.lower():
            print (lyric + " includes tracklist or album art")
            #os.remove(lyric_path)
            removal_list.append(lyric_path)
            shutil.move(clean_directory + '/' + lyric, scraper.artist_directory + '/tracklist_album_art' + '/' + lyric)
    for lyric in os.listdir(clean_directory):
        if "remix" in lyric.lower():
            print (lyric + " includes remix")
            if lyric_path not in removal_list:
                removal_list.append(lyric_path)
            shutil.move(clean_directory + '/' + lyric, scraper.artist_directory + '/remix' + '/' + lyric)
    for lyric in os.listdir(clean_directory):
        if os.path.getsize(lyric_path) <= 200:
            print (lyric + " size is smaller than 200 bytes")
            #os.remove(lyric_path)
            if lyric_path not in removal_list:
                removal_list.append(lyric_path)
            shutil.move(clean_directory + '/' + lyric, scraper.artist_directory + '/small' + '/' + lyric)
            
#==============================================================================
#     for path in removal_list:
#         os.remove(path)
#==============================================================================
    return removal_list
    
def iso_artist_lyrics(scraper):
    artist = scraper.artist
    create_new_directory(scraper)    
    clean_directory = scraper.artist_directory + '/clean'
    for file in os.listdir(clean_directory):
        file_path = clean_directory + '/' + file
        words_orig = open(file_path).read()
        del_index_list = []
        d = '['
        
        words_split = [e + d for e in words_orig.split('[') if e != '']
        for i in range(len(words_split)):
            words_split_line = words_split[i].split('\n')
            if (':' in words_split_line[0] or '-' in words_split_line[0]):
                if artist not in words_split_line[0]:
                    del_index_list.append(i)
        new_words_split = []
        for i in range(len(words_split)):
            if i not in del_index_list:
                new_words_split.append(words_split[i])
        new_words_split = ''.join(new_words_split)
        new_words_split = new_words_split[:-2]
        
        
        wr = open(file_path, 'w')
        wr.write(new_words_split)
        wr.close()
    
    for file in os.listdir(clean_directory):
        file_path = clean_directory + '/' + file
        if os.path.getsize(file_path) < 50:
            shutil.move(file_path, scraper.artist_directory + '/small')

        
        
    
    