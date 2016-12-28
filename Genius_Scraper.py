# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 21:26:06 2016

@author: Javesh
"""

import requests
from bs4 import BeautifulSoup
import os, json
import string
import pandas as pd


BASE_URL = "http://api.genius.com"
proxies = [{"http": "http://124.88.67.81"}, {"http": "http://124.88.67.52"}, {"http": "http://124.88.67.17"}]
headers = {'Authorization': 'Bearer [insert you bearer token here]'}

class Genius_Scraper:
    def __init__(self, artist, albums):
        #artist is the artist name for which you want songs
        #albums is the list of albumbs for which you want songs
        self.artist = artist
        self.albums = [album.lower() for album in albums]
        self.lyrics_df = self.compile_lyrics()
        
    def strip(s):
        s = s.replace('?', '')
        s = s.replace('*', '')
        s = s.replace('/', '_')
        s = s.replace('(', '')
        s = s.replace(')', '')
        s = s.replace('"', '')
        return s
            
    
    def get_artist_api_path(self, artist_name):
        """
        Find the artists id on Genius by accessing a song by the artist via
        the artist's page on Genius. This id is then made into the api path
        and returned by the function.
        """
        search_url = BASE_URL + "/search"
        data = {'q': artist_name}
        response = requests.get(search_url, data=data, headers=headers, proxies = proxies)
        artist_info = response.json()
        for hit in artist_info["response"]["hits"]:
            song_api_path = hit["result"]["api_path"]
            song_url = BASE_URL + song_api_path
            response_2 = requests.get(song_url, headers=headers, proxies = proxies)
            new_json = response_2.json()
            artist = new_json["response"]["song"]["primary_artist"]
            if (artist["name"]) == (artist_name):
                artist_api_path = artist["api_path"]
                return artist_api_path
                break
            else:
                print ("Could not find %s" % artist_name)                
                return None
        
    def get_song_api_paths(self, artist_api_path):
        song_api_paths = []
        artist_url = BASE_URL + artist_api_path + "/songs"
        data = {"per page":50, "page":1}
        while True:
            response = requests.get(artist_url, data=data, headers=headers, proxies = proxies)
            new_json = response.json()
            songs = new_json["response"]["songs"]
            for song in songs:
                if song['primary_artist']['api_path'] == artist_api_path:
                    song_api_paths.append(song["api_path"])
                else:
                    continue
            if len(songs) < 50:
                break
            else:
                if "page" in data:
                    data["page"] = data["page"] + 1
                else:
                    break
        return list(set(song_api_paths))
            
    def get_song_info(self, song_api_path):
        song_url = BASE_URL + song_api_path
        response = requests.get(song_url, headers=headers, proxies = proxies)
        full_song_info = response.json()
        return full_song_info
        
    def get_song_title(self, song_api_path):
                
        full_song_info = self.get_song_info(song_api_path)
        song_title = full_song_info["response"]["song"]["title"]
        return song_title
    
    def get_song_title_path(self, song_api_path):
        song_title = self.get_song_title(song_api_path)
        song_title = song_title.replace(' ', '_')
        song_title = song_title.replace('/', '_')
        return song_title
        
    def get_song_web_path(self, song_api_path):
        full_song_info = self.get_song_info(song_api_path)
        song_web_path = full_song_info["response"]["song"]["path"]
        return song_web_path      
        
    def get_lyrics(self, song_api_path):
        song_web_path = self.get_song_web_path(song_api_path)
        page_url = "http://genius.com" + song_web_path
        page = requests.get(page_url, proxies=proxies)
        html = BeautifulSoup(page.text, "html.parser")
        [h.extract() for h in html('script')]
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
        lyrics = lyrics.replace("\n", "")
        lyrics = lyrics.replace("\r", "")
        return lyrics
    """    
    def song_ids_already_scraped(self, artist_folder_path, force=False):
        #check for ids already scraped so we don't redo
      if force:
        return []
      song_ids = []
      files = os.listdir(artist_folder_path)
      for file_name in files:
        dot_split = file_name.split('.')
        #sometimes the file is empty, we don't want to include if that's the case
        if dot_split[1] == 'txt':
          try:
            song_id = dot_split[0].split("_")[-1]
            if os.path.getsize(artist_folder_path + '/' + file_name) != 0:
              song_ids.append(song_id)
          except:
            pass
        return song_ids
    """
    
    def create_lyrics_txt(self):
        for artist_name in self.artists:
            artist_folder_path = "artists/%s" % artist_name
            artist_lyrics_path = "%s/lyrics" % artist_folder_path
            artist_info_path = "%s/info" % artist_folder_path
            
            if not os.path.exists(artist_folder_path):
                os.makedirs(artist_folder_path)
            if not os.path.exists(artist_lyrics_path):
                os.makedirs(artist_folder_path)
            if not os.path.exists(artist_info_path):
                os.makedirs(artist_info_path)
            
            artist_api_path = self.get_artist_api_path(artist_name)
            song_api_paths = self.get_song_api_paths(artist_api_path)
            
            for path in song_api_paths:
                full_song_info = self.get_song_info(path)                
                
                song_title_path = self.get_song_title_path(path)
                print(song_title_path)
                song_web_path = self.get_song_web_path(path)
                
                cleaned_lyrics = self.clean_lyrics(song_web_path)
                
                lyric_path = "%s/lyrics/%s.txt" % (artist_folder_path, song_title_path)
                info_path = "%s/info/%s.txt" % (artist_folder_path, song_title_path)
                
                print(lyric_path)
                
                with open(info_path, "w") as lfile:
                    lfile.write(json.dumps(full_song_info))
                with open(lyric_path, "w") as ifile:
                    try:
                        ifile.write(cleaned_lyrics)
                    except UnicodeEncodeError as error:
                        print (error)
                        
                        
    def compile_lyrics(self):
        """artist = []        
        song = []        
        lyrics = []
        """
        lyrics_df= pd.DataFrame()
        """
        for artist_name in self.artists:
            artist = []            
            song = []
            lyrics = []
            artist_path = self.get_artist_api_path(artist_name)            
            for path in self.get_song_api_paths(artist_path):
                if self.get_song_info(path)["response"]["song"]["album"]["name"] in self.albums:                
                    print (self.get_song_title(path))
                    song.append(self.get_song_title(path))
                    lyrics.append(self.clean_lyrics(path))
                    print ('Done!')
            artist = [artist_name] * len(song)
            #temp_dict = {'Artist': artist, 'Song': song, 'Lyrics': lyrics}
            temp_df = pd.DataFrame({'Artist': artist, 'Song': song, 'Lyrics': lyrics})
            print (temp_df)
            lyrics_df = lyrics_df.append(other = temp_df)
        return lyrics_df
        """                
        artist_name = self.artist
        album = []               
        song = []
        lyrics = []
        artist_path = self.get_artist_api_path(artist_name)            
        for path in self.get_song_api_paths(artist_path):
            #if self.get_song_info(path)["response"]["song"]["album"]["name"] != None:    
            try:
                if self.get_song_info(path)["response"]["song"]["album"]["name"].lower() in self.albums:                
                    print (self.get_song_title(path) + 'Downloading!')
                    album.append(self.get_song_info(path)["response"]["song"]["album"]["name"])
                    song.append(self.get_song_title(path))
                    lyrics.append(self.clean_lyrics(path))
                    print ('Done!')
                else:
                    print (self.get_song_title(path) + ' is not in any of the albums!')
            except (TypeError) as e:
                print(e)                
                continue
        #artist = [artist_name] * len(song)
        #temp_dict = {'Artist': artist, 'Song': song, 'Lyrics': lyrics}
        #temp_df = pd.DataFrame({'Artist': artist, 'Song': song, 'Lyrics': lyrics})
        #print (temp_df)
        lyrics_df = pd.DataFrame({'Album': album, 'Song': song, 'Lyrics': lyrics})
        return lyrics_df    
            
        
        
                
        
        


