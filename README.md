# HCIFacebook

Reupload for public version

Use: Parses Facebook's zip of information on you to create interactive visualizations of the data they know about you

To obtain your Facebook zip: Facebook settings > Your Facebook information > Download your information > Tick all boxes and request a download

Visualizations: Friends, IP locations logged in from, Groups interacted with, Marketing Profile, Apps sharing data with Facebook, Number of messages and photos on file

To Run: Streamlit run Streamlit.py

or loader on its own: python Loader.py

I don't know if HTMLParser is the best way to get the data out, probably faster with just regex

Loader.py: Turns facebook files into panda data frames

Streamlit.py: Turns panda frames into graphs and puts it in browser

Facebook_info_stripped: File containing facebook files that have been stripped/filled with dummy data, Probably best to use your own data while testing and not upload it to this repo
