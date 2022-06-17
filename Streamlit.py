import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from vega_datasets import data as vega_data
import json
#import geopandas as gpd

from urllib.error import URLError
import Loader
import FakeLoader
import pydeck as pdk
from PIL import Image

st.set_page_config(layout="wide")

if 'clicked' not in st.session_state:
    st.session_state['clicked'] = False

def ButtonClicked():
    try:
        #Get profile info
        profile = FakeLoader.get_Profile_Information()
        
        #Title
        #Title ui
        st.title('Facebook info on ' + profile['name'])

        #Profile info gonna hard code to save time
        profile2 = {}
        profile2['Name'] = "Ted Jones"
        profile2['Email'] = "tedjones@gmail.com"
        profile2['Phone'] = "+30405050040"
        profile2['DoB'] = "23/05/1998"
        profile2['City'] = "Paris, France"
        profile_frame = pd.DataFrame([profile2],index=['Your Information'])
        st.table(profile_frame)

        #Family information
        st.subheader("Family")

        col1, col2 = st.columns((2,2))
        
        with col1:
            st.write("Barry Jones (Brother):")
            image = Image.open('Facebook_info_stripped\\messages\\photos\\brother.jpg')
            st.image(image)
        with col2:
            st.write("Emma Jones (Sister):")
            image2 = Image.open('Facebook_info_stripped\\messages\\photos\\sister.jpg')
            st.image(image2)
        
        #Page layout
        col1, col2 = st.columns((2,2))

        with col1:
            #Group interactions graph
            st.subheader("Interactions in Groups")
            df = Loader.parse_Group_Interactions()
            data = df.reset_index()
            chart = (
                    alt.Chart(data)
                    .mark_bar()
                    .encode(
                        y="pages",
                        x="Interactions"
                    )
                )
            st.altair_chart(chart, use_container_width=True)

            #Off facebook activity graph
            st.subheader("Shared Data With Facebook")
            df = Loader.parse_Off_Facebook_Activity()
            data = df.reset_index()
            chart = (
                    alt.Chart(data)
                    .mark_bar()
                    .encode(
                        y="name",
                        x="times"
                    )
                )
            st.altair_chart(chart, use_container_width=True)

            #Radar Chart
            st.subheader("Market Profile")
            market_profile = FakeLoader.get_Market_Profile()
            labels=['Creative', 'Sports', 'Media', 'Relationship', 'Occupation', 'Other']
            stats=[4,10,6,3,2,2]
            examples=[["Painter","Singer"], ["Rugby","Boxing","Hiking"], ["Breaking Bad","Beatles"], ["Son","Brother"], ["Student","Computer Science"], ["Travel","Food and Drink"]]
            angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False) # Set the angle
            # close the plot

            params = {"ytick.color" : "black",
            "xtick.color" : "w",
            "axes.labelcolor" : "w",
            "axes.edgecolor" : "w"}
            plt.rcParams.update(params)
            
            stats_loop=np.concatenate((stats,[stats[0]]))  # Closed
            angles_loop=np.concatenate((angles,[angles[0]]))  # Closed
            fig=plt.figure()
            fig.patch.set_facecolor((0,0,0,0)) #Color to match streamlit

            ax = fig.add_subplot(111, polar=True)   # Set polar axis
            line = ax.plot(angles_loop, stats_loop, 'o-', linewidth=2)  # Draw the plot (or the frame on the radar chart)
            ax.fill(angles, stats, alpha=0.25)  #Fulfill the area
            ax.set_facecolor('xkcd:white') #Color
            ax.set_thetagrids(angles * 180/np.pi, labels)  # Set the label for each axis
            #ax.set_rlim(0,250)
            ax.tick_params(axis='both', which='major', pad=25)
            ax.grid(True)
            st.pyplot(fig)

            #Radio to see underlying data
            category = st.radio("Breakdown",('Media','Sports','Relationship','Creative','Occupation','Other'))
            if(category == 'Creative'):
                st.write("Creative intrests: Painting, singing, dancing, and Bob Ross")
            elif(category == 'Sports'):
                st.write("Sport intrests: Rugby, Boxing, Hiking, Muay Thai, Basketball, FC Barcelona, MotorSports, La Liga, MLB, and Nike")
            elif(category == 'Media'):
                st.write("Media intrests: Breaking Bad, The Beatles, Visual Arts, Fantasy, Animation, and Video Games")
            elif(category == 'Other'):
                st.write("Other intrests: Travel, Food and Drink")
            elif(category == 'Occupation'):
                st.write("Occupation: Student and Computer Science")
            elif(category == 'Relationship'):
                st.write("Relationships: Brother (aged 37), Sister (aged 30), Fathers Day Gifts")

        with col2:
            #Ip graph
            st.subheader("Locations Logged")
            df = Loader.get_IP_Lat_Long_Fake()
            url = "https://raw.githubusercontent.com/deldersveld/topojson/master/countries/united-kingdom/uk-counties.json"
            states = alt.topo_feature(url, feature="GBR_adm2")
            countries = alt.topo_feature(vega_data.world_110m.url, 'countries')

            background = alt.Chart(states).mark_geoshape(
                fill='#666666',
                stroke='white'
            ).properties(
                width=400, height=300
            )
            points = alt.Chart(df).mark_circle().encode(
                longitude='lon:Q',
                latitude='lat:Q',
                size=alt.Size('count:Q',title="Count"),
                color=alt.value('steelblue'),
                tooltip=['city:N','ip:N','count:Q']
            )
            union = background+points
            #Streamlit build in map
            st.map(df)
            #Streamlit with altair map
            st.subheader("Interaction Overview")
            st.altair_chart(union,use_container_width=True)

            #Donut messages chart
            st.subheader("Saved Information")
            source = pd.DataFrame({"Type": ["Messages (400)", "Photos (60)", "Videos (10)"], "value": [400, 60, 10]})
            chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="value", type="quantitative"),
                color=alt.Color(field="Type", type="nominal"),
            )
            #requires pip install altair==4.2.0rc1
            st.altair_chart(chart,use_container_width=True)

        #Pydeck chart
        st.header('IP logs')
        chart = pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=52,
                longitude=-1,
                zoom=8,
                pitch=50
            ),
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=df,
                    get_position=['lon','lat'],
                    radius=8000,
                    get_elevation='count',
                    elevation_range=[1000,50000],
                    pickable=True,
                    extruded=True,
                )
            ],
            tooltip = {"html": "<b>Count:</b> {elevationValue}"}
        )
        
        st.pydeck_chart(chart)       
    except URLError as e:
        st.error(
            """
            **Internet connection error.**

            Connection error: %s
        """
            % e.reason
        )

#Reload the graphs if already clicked
if(st.session_state['clicked'] == True):
    ButtonClicked()

#Pre graph title
st.title("Please upload a zip file requested from facebook")

def setButtonClicked():
    st.session_state['clicked'] = True

#File uploader ui
#Doesn't actually do anything but shows intended functionality
uploaded_file = st.file_uploader("Choose a file", help="This should be a zip file requested from facebook. Settings and Privacy -> Settings -> Your Facebook Information -> Download your information")
button = st.button("Display", setButtonClicked())