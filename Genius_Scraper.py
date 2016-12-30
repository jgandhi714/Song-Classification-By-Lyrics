# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 22:30:05 2016

@author: Javesh
"""
import requests
import json
from bs4 import BeautifulSoup
import os
#from difflib import SequenceMatcher as sm
import shutil
from collections import Counter
import string
import scipy
import matplotlib.pyplot as plt
import re
import random
import math

BASE_URL = 'http://api.genius.com'
headers = {'Authorization': 'Bearer [insert bearer token here]'}

class Genius_Scraper:
    def __init__(self, artist, albums):
        self.artist = artist
        self.albums = albums
        self.albums_lower = [album.lower() for album in albums]
        self.artist_api_path = self.get_artist_api_path()
        self.artist_directory = "artists/%s" % self.artist
        self.lyrics_directory = self.artist_directory + "/lyrics"
        self.clean_directory = self.artist_directory + "/clean"
        self.training_directory = self.artist_directory + "/random/training"
        self.test_directory = self.artist_directory + "/random/test"
        
    
    def strip(self, s):
        s = s.replace('?', '')
        s = s.replace('*', '')
        s = s.replace('/', '_')
        s = s.replace('(', '')
        s = s.replace(')', '')
        s = s.replace('"', '')
        return s
        
    def get_artist_api_path(self):
        """
        Find the artist id on Genius by accessing a song by the artist via 
        the artist's page on Genius. This id is then made into the api path
        and returned by the function
        """
        artist = self.artist
        search_url = BASE_URL + "/search"
        data = {'q': artist}
        response = requests.get(search_url, data=data, headers=headers)
        artist_info = response.json()
        #keep looping through the artists hits until it is confirmed that we have the right artist api path 
        for hit in artist_info["response"]["hits"]:
            song_api_path = hit["result"]["api_path"]
            song_url = BASE_URL + song_api_path
            response = requests.get(song_url, headers=headers)
            song_info = response.json()
            artist_name = song_info["response"]["song"]["primary_artist"]
            if artist_name["name"] == artist:
                return artist_name["api_path"]
            else:
                return None
                
    def get_song_info(self, song_api_path):
        song_url = BASE_URL + song_api_path
        response = requests.get(song_url, headers=headers)
        full_song_info = response.json()
        return full_song_info
    
    def get_song_title(self, song_api_path):
        full_song_info = self.get_song_info(song_api_path)
        song_title = full_song_info["response"]["song"]["title"]
        return song_title
    
    def get_song_web_path(self, song_api_path):
        full_song_info = self.get_song_info(song_api_path)
        song_web_path = full_song_info["response"]["song"]["path"]
        return song_web_path
    
    def get_lyrics(self, song_api_path):
        song_web_path = self.get_song_web_path(song_api_path)
        lyrics_url = "http://genius.com" + song_web_path
        lyrics = requests.get(lyrics_url)
        html = BeautifulSoup(lyrics.text, "html.parser")
        [h.extract for h in html('script')]
        lyrics = html.find("lyrics").get_text()
        return lyrics
    
    def clean_lyrics(self, song_api_path):
        lyrics = self.get_lyrics(song_api_path)
        lyrics = lyrics.replace(u"\u2019", "'") #right quotation mark
        lyrics = lyrics.replace(u"\u2018", "'") #left quotation mark
        lyrics = lyrics.replace(u"\u02bc", "'") #a with dots on top
        lyrics = lyrics.replace(u"\xe9", "e") #e with an accent
        lyrics = lyrics.replace(u"\xe8", "e") #e with an backwards accent
        lyrics = lyrics.replace(u"\xe0", "a") #a with an accent
        lyrics = lyrics.replace(u"\u2026", "...") #ellipsis apparently
        lyrics = lyrics.replace(u"\u2012", "-") #hyphen or dash
        lyrics = lyrics.replace(u"\u2013", "-") #other type of hyphen or dash
        lyrics = lyrics.replace(u"\u2014", "-") #other type of hyphen or dash
        lyrics = lyrics.replace(u"\u201c", '"') #left double quote
        lyrics = lyrics.replace(u"\u201d", '"') #right double quote
        lyrics = lyrics.replace(u"\u200b", ' ') #zero width space ?
        lyrics = lyrics.replace(u"\x92", "'") #different quote
        lyrics = lyrics.replace(u"\x91", "'") #still different quote
        lyrics = lyrics.replace(u"\xf1", "n") #n with tilde!
        lyrics = lyrics.replace(u"\xed", "i") #i with accent
        lyrics = lyrics.replace(u"\xe1", "a") #a with accent
        lyrics = lyrics.replace(u"\xea", "e") #e with circumflex
        lyrics = lyrics.replace(u"\xf3", "o") #o with accent
        lyrics = lyrics.replace(u"\xb4", "") #just an accent, so remove
        lyrics = lyrics.replace(u"\xeb", "e") #e with dots on top
        lyrics = lyrics.replace(u"\xe4", "a") #a with dots on top
        lyrics = lyrics.replace(u"\xe7", "c") #c with squigly bottom
        #lyrics = lyrics.replace("\n", "")
        #lyrics = lyrics.replace("\r", "")
        return lyrics
    
    def create_txt(self):
        #set up directories to store txt files
        lyrics_folder_path = "artists/%s" % self.artist + '/lyrics'
        if not os.path.exists(lyrics_folder_path):
            os.makedirs(lyrics_folder_path)
        
        blank_folder_path = lyrics_folder_path + '/blank'
        if not os.path.exists(blank_folder_path):
            os.makedirs(blank_folder_path)
        
        artist_api_path = self.artist_api_path
        artist_songs_url = BASE_URL + artist_api_path + "/songs"
        #iterate through as many pages as possible - once an error is hit, break from the loop        
               
        for i in range(1, 1000):
            j = str(i)            
            
            try:  
                data = {"page": i}
                response = requests.get(artist_songs_url, data=data, headers=headers)
                try:                
                    artist_songs_info = response.json()
                except(IndexError):
                    print ("ALL DONE!!!")
                    break
                songs = artist_songs_info["response"]["songs"]
                
                #check to see if we already have the text files from this page and skip it if so in order to let us
                #start at the page we left off (in case of connection break from earlier download session)
                try:                
                    check_song = songs[-1]
                    print("ON PAGE " + j)
                except(IndexError):
                    print ("ALL DONE!!!")                    
                    break
                
                check_song_api_path = check_song["api_path"]
                check_song_title = self.get_song_title(check_song_api_path)
                check_lyric_path = lyrics_folder_path + '/%s' % self.strip(check_song_title) + '.txt'
                check_blank_path = blank_folder_path + '/%s' % self.strip(check_song_title) + '.txt'
                if os.path.exists(check_lyric_path) or os.path.exists(check_blank_path):
                    print("SKIPPING PAGE " + j)
                    continue
                
                for song in songs:
                    song_api_path = song["api_path"]
                    song_title = self.get_song_title(song_api_path)
                    lyric_path = lyrics_folder_path + '/%s' % self.strip(song_title) + '.txt'
                    blank_path = blank_folder_path + '/%s' % self.strip(song_title) + '.txt'
                    
                    #check if primary artist is the right one`
                    if song['primary_artist']['api_path'] == artist_api_path:
                        try:
                            #check if song is in list of albums
                            if self.get_song_info(song_api_path)["response"]["song"]["album"]["name"].lower() in self.albums_lower:
                                #check if already downloaded                                
                                if not os.path.exists(lyric_path):
                                    print(".......CREATING TXT FILE " + song_title)
                                    lyrics = self.clean_lyrics(song_api_path)                                    
                                    with open(lyric_path, "w") as ifile:
                                        try:
                                            ifile.write(lyrics)
                                        except UnicodeEncodeError as e:
                                            print(e)
                                else:
                                    if os.path.getsize(lyric_path) == 0:
                                        print(".......CREATING TXT FILE " + song_title)
                                        lyrics = self.clean_lyrics(song_api_path)                                    
                                        with open(lyric_path, "w") as ifile:
                                            try:
                                                ifile.write(lyrics)
                                            except UnicodeEncodeError as e:
                                                print(e)
                                                continue
                                    else:
                                        print("TXT FILE ALREADY EXISTS FOR " + song_title)
                            else:
                                open(blank_path, 'a').close()
                                continue
                        except (TypeError, ValueError):
                            #print(self.get_song_title(song_api_path) + " album could not be found!")
                             open(blank_path, 'a').close()                            
                             continue
                    else:
                        open(blank_path, 'a').close()
                        continue
            
            except():
                break
            
        return os.listdir(lyrics_folder_path)
        
    def create_new_directory(self):
        #creates new directory called clean and copies every lyric file
        clean_directory = self.artist_directory + '/clean'    
        if not os.path.exists(clean_directory):
            os.makedirs(clean_directory)
            for lyric in os.listdir(self.lyrics_directory):
                if os.path.isfile(self.lyrics_directory + '/' + lyric):
                    shutil.copy(self.lyrics_directory + '/' + lyric, clean_directory + '/' + lyric)
    
    def remove_extras(self):
        #removes files like tracklist and remix files scraped from Genius
        self.create_new_directory()    
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
                shutil.move(clean_directory + '/' + lyric, self.artist_directory + '/remix' + '/' + lyric)
                
        for lyric in os.listdir(clean_directory):
            if os.path.getsize(lyric_path) <= 200:
                print (lyric + " size is smaller than 200 bytes")
                #os.remove(lyric_path)
                if lyric_path not in removal_list:
                    removal_list.append(lyric_path)
                shutil.move(clean_directory + '/' + lyric, self.artist_directory + '/small' + '/' + lyric)
                
    #==============================================================================
    #     for path in removal_list:
    #         os.remove(path)
    #==============================================================================
        return removal_list
        
    def iso_artist_lyrics(self):
        artist = self.artist
        self.create_new_directory()    
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
                shutil.move(file_path, self.artist_directory + '/small')
                
    def master_clean(self):
        self.remove_extras()
        self.iso_artist_lyrics()
        
    def create_random_directories(self, training_data_size = 0):
        random_training_directory = self.artist_directory + '/random/training'
        random_test_directory = self.artist_directory + '/random/test'        
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
            directory_length = len(os.listdir(self.clean_directory))            
            training_data_size = math.ceil(0.6 * directory_length)
            
        while training_set == None or len(training_set) < training_data_size:
            chosen_file = random.choice(os.listdir(self.clean_directory))
            #chosen_path = scraper.clean_directory + '/' + chosen_file
            training_set.add(chosen_file)
        for file in training_set:
            shutil.copy(self.clean_directory + '/' + file, random_training_directory + '/' + file)
        for file in os.listdir(self.clean_directory):
            if file not in training_set:
                test_set.add(file)
        for file in test_set:
            shutil.copy(self.clean_directory + '/' + file, random_test_directory + '/' + file)
        
            
        
        print('training set:' + training_set + ', test set:' + test_set)
            
