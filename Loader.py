import pandas as pd
from html.parser import HTMLParser
import re
import os
from os.path import join, getsize
import glob
from collections import Counter

data_list = []
attrs_list = []

class customHTMLParser(HTMLParser):
    def handle_data(self, data):
        if(data == ' ' or data == '\'' or data == ''):
            return
        data_list.append(data)
    def handle_starttag(self, tag, attrs):
        if(tag == 'a' and attrs[0][0] == "href"):
            attrs_list.append(attrs[0][1])
    def reset_lists(self):
        data_list.clear()
        attrs_list.clear()

def parse_Group_Interactions():
    file = open('Facebook_info_stripped/activity_messages/group_interactions.html', mode='r')
    data = file.read()
    file.close()
    parser = customHTMLParser()
    parser.reset_lists()
    parser.feed(data)
    group_interactions = {}
    group_interactions['pages'] = data_list[7:-2:2]
    counts = []
    for string in data_list[8:-2:2]:
        try:
            counts.append(int(re.findall("[0-9]+", string)[0]))
        except:
            print("Regex error for:")
            print(string)
    group_interactions['Interactions'] = counts
    group_interactions['links'] = attrs_list[::2]
    df = pd.DataFrame(data = group_interactions)
    df.set_index('pages')
    return(df)

def parse_Off_Facebook_Activity():
    files = glob.glob('Facebook_info_stripped/apps_and_websites_off_of_facebook/your_off-facebook_activity/*')
    worst_offenders = []
    for f in files:
        offender = parse_Off_Facebook_Activity_Event(f)
        if(offender['times'] > 10):
            worst_offenders.append(offender)
    df = pd.DataFrame(worst_offenders, columns=['name','times'])
    return(df)
        
def parse_Off_Facebook_Activity_Event(f):
    file = open(f)
    data = file.read()
    file.close()
    parser = customHTMLParser()
    parser.reset_lists()
    parser.feed(data)
    name = data_list[7].replace("Activity received from ", '')
    offender = {}
    offender['name'] = name
    offender['times'] = len(data_list[8:-2:6])
    return offender

def parse_IP_Adresses():
    file = open('Facebook_info_stripped/security_and_login_information/account_activity.html', mode='r')
    data = file.read()
    file.close()
    ips = re.findall("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", data)
    #count duplicates
    ip_dict = Counter(ips)
    locations = get_IP_Lat_Long(ip_dict)
    df = pd.DataFrame(locations)
    return(df)

import requests

#real
def get_IP_Lat_Long(ip_dict):
    url = "https://api.ipgeolocation.io/ipgeo?apiKey=aa57943214bf44e2ab68e6a37e6c34be&ip="
    locations = []
    counter = 0
    for ip,count in ip_dict.items():
        data = {}
        
        #only look at high counts for this
        if(count<100):
            continue
        #stop at 100 lookups to save requests
        if(counter > 100):
            break
        response = requests.get(url+ip+"&fields=geo")
        if(response.status_code == 200):
            info = response.json()
            data['count'] = count
            data['lat'] = float(info['latitude'])
            data['lon'] = float(info['longitude'])
            #data['city'] = info['city']
            #data['ip'] = ip
            locations.append(data)
    print(locations)
    return(locations)

#fake copy of get_IP_Lat_Long that uses pre stored data to save api requests
def get_IP_Lat_Long_Fake():
    data = [{'count': 3, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 18, 'lat': 51.50115, 'lon': -0.09951, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 12, 'lat': 51.42296, 'lon': -2.85082, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 3, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 3, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.41693, 'lon': -1.31908, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.52429, 'lon': -0.07145, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 57, 'lat': 51.42296, 'lon': -2.85082, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 3, 'lat': 51.42296, 'lon': -2.85082, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.42296, 'lon': -2.85082, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 
'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 9, 'lat': 51.42296, 'lon': -2.85082, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 14, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 13, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.42388, 'lon': -0.9876, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 51.46194, 'lon': -0.97421, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 1, 'lat': 51.60999, 'lon': -0.24436, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 3, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 4, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 5, 'lat': 51.50115, 'lon': -0.09951, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 5, 'lat': 51.41693, 'lon': -1.31908, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 3, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 16, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 
'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}, {'count': 2, 'lat': 52.48624, 'lon': -1.8904, 'city':"Bristol", 'ip': "106.101.123.403"}]
    df = pd.DataFrame(data)
    return(df)