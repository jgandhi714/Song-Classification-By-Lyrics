# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 15:49:38 2016

@author: Javesh
"""

import Genius_Scraper as GS
import os
import shutil

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
    removal_list = []    
    clean_directory = scraper.artist_directory + '/clean'    
    for lyric in os.listdir(clean_directory):
        lyric_path = clean_directory + '/' + lyric        
        if "tracklist" in lyric.lower() or "album art" in lyric.lower():
            print (lyric + " includes tracklist or album art")
            #os.remove(lyric_path)
            removal_list.append(lyric_path)
        if "remix" in lyric.lower():
            print (lyric + " includes remix")
            if lyric_path not in removal_list:
                removal_list.append(lyric_path)
        if os.path.getsize(lyric_path) <= 200:
            print (lyric + " size is smaller than 200 bytes")
            #os.remove(lyric_path)
            if lyric_path not in removal_list:
                removal_list.append(lyric_path)
    for path in removal_list:
        os.remove(path)
    return removal_list
"""
def iso_artist_lyrics(scraper):
    directory = scraper.directory
    path = directory + '/clean'
    if not os.path.exists(path):
        os.makedirs(path)
"""
    
    