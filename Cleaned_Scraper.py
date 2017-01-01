# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:43:37 2016

@author: Javesh
"""
import os 
import shutil 
from Genius_Scraper import Genius_Scraper

class Cleaned_Scraper(Genius_Scraper):
    
    def __init__(self, artist, albums, run_scraper = 'no'):
        Genius_Scraper.__init__(self, artist, albums, run_scraper)
        self.clean_directory = self.artist_directory + "/clean"        
        try:        
            self.master_clean()
        except(FileNotFoundError):
            self.create_txt()
            self.master_clean()
        self.removal_list = self.remove_extras()
        
        
    def create_clean_directory(self):
        #creates new directory called clean and copies every lyric file
        clean_directory = self.artist_directory + '/clean'    
        if not os.path.exists(clean_directory):
            os.makedirs(clean_directory)
        for lyric in os.listdir(self.lyrics_directory):
            if os.path.isfile(self.lyrics_directory + '/' + lyric):
                shutil.copy(self.lyrics_directory + '/' + lyric, clean_directory + '/' + lyric)
                    
    def remove_extras(self):
        #removes files like tracklist and remix files scraped from Genius
        self.create_clean_directory()    
        removal_list = []    
        if not os.path.exists(self.artist_directory + '/tracklist_album_art'):
            os.makedirs(self.artist_directory + '/tracklist_album_art')
        
        if not os.path.exists(self.artist_directory + '/remix'):
            os.makedirs(self.artist_directory + '/remix')
        
        if not os.path.exists(self.artist_directory + '/small'):
            os.makedirs(self.artist_directory + '/small')
            
        clean_directory = self.artist_directory + '/clean'    
        
        for lyric in os.listdir(clean_directory):
            lyric_path = clean_directory + '/' + lyric        
            if "tracklist" in lyric.lower() or "album art" in lyric.lower() or "[" in lyric.lower():
                print (lyric + " includes tracklist, album art, etc.")
                #os.remove(lyric_path)
                removal_list.append(lyric_path)
                shutil.move(clean_directory + '/' + lyric, self.artist_directory + '/tracklist_album_art' + '/' + lyric)
        for lyric in os.listdir(clean_directory):
            if "remix" in lyric.lower():
                print (lyric + " includes remix")
                if lyric_path not in removal_list:
                    removal_list.append(lyric_path)
                shutil.move(clean_directory + '/' + lyric, self.artist_directory + '/remix/' + lyric)
                
        for lyric in os.listdir(clean_directory):
            if os.path.getsize(lyric_path) <= 200:
                print (lyric + " size is smaller than 200 bytes")
                #os.remove(lyric_path)
                if lyric_path not in removal_list:
                    removal_list.append(lyric_path)
                shutil.move(clean_directory + '/' + lyric, self.artist_directory + '/small/' + lyric)
        return removal_list
        
    def iso_artist_lyrics(self):
        artist = self.artist
        self.create_clean_directory()    
        clean_directory = self.artist_directory + '/clean'
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
                try:                
                    shutil.move(file_path, self.artist_directory + '/small')
                except:
                    os.remove(file_path)
                
    def master_clean(self):
        self.remove_extras()
        self.iso_artist_lyrics()