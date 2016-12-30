# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:30:21 2016

@author: Javesh
"""
import Genius_Scraper as GS

class NB_Classifier:
    def __init__(self,list_of_GS):
        self.list_of_GS = list_of_GS
    
    def create_test_training_set(self):
        for GS_instance in self.list_of_GS:
            GS_instance.create_random_directories()
    
    
        