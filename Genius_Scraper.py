# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 22:30:05 2016

@author: Javesh
"""
import requests
import json
from bs4 import BeautifulSoup
import os

BASE_URL = 'http://api.genius.com'
headers = {'Authorization': 'Bearer 1fD64UHpd-b-JoPbyL-zmhmweu-VXSPU3HGQ0Nw9EoSiGvAa6HHEwaV2n2rHj55D'}

class Genius_Scraper:
    def __init__(self, artist, albums, run_scraper = False):
        self.artist = artist
        self.albums = albums
        self.albums_lower = [album.lower() for album in albums]
        self.artist_api_path = self.get_artist_api_path()
        self.artist_directory = "artists/%s" % self.artist
        self.lyrics_directory = self.artist_directory + "/lyrics"
        if run_scraper == True:
            self.create_txt()

            
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
        for i in range(1, 100000):
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
 