import pandas as pd
from html.parser import HTMLParser
import re
import os
from os.path import join, getsize
import glob
from collections import Counter

def get_Profile_Information():
    profile = {}
    profile['name'] = "Ted Jones"
    profile['email'] = "tedjones@gmail.com"
    profile['phone'] = "+30405050040"
    profile['dob'] = "23/05/1998"
    profile['city'] = "Paris, France"
    profile['family'] = [
        {'name': 'Barry Jones', 'relation': 'Father'},
        {'name': 'Garry Jones', 'relation': 'Brother'}
        ]
    profile['education'] = [
        "Massachusetts Institute of Technology",
        "University of Sydney"
        ]
    profile['donor'] = "Unregistered"
    return(profile)

def get_Market_Profile():
    market_profile = {}
    market_profile['Creative'] = {'count': 4, 'examples': ["Painter","Singer"]}
    market_profile['Sports'] = {'count': 10, 'examples': ["Rugby","Boxing","Hiking"]}
    market_profile['Media'] = {'count': 6, 'examples': ["Breaking Bad","Beatles"]}
    market_profile['Relationship'] = {'count': 3, 'examples': ["Son","Brother"]}
    market_profile['Occupation'] = {'count': 2, 'examples': ["Student","Computer Science"]}
    market_profile['Other'] = {'count': 2, 'examples': ["Travel","Food and Drink"]}
    return(market_profile)
