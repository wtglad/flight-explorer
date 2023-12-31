import streamlit as st 
import pandas as pd
import pydeck as pdk 

# This isn't pretty but it does allow user to search origin airport and see connecting direct flights. Only covers US for now. 

df = pd.read_csv('data/clean_flight_data.csv')

with st.sidebar: 
	selected_origin = st.selectbox('Select origin airport', options=df['search_airport'].drop_duplicates())


results_df = df[df['search_airport'] == selected_origin]

arc_layer = pdk.Layer(
    "ArcLayer",
    data=results_df,
    #get_width="S000 * 2",
    get_source_position=["longitude_origin", "latitude_origin"],
    get_target_position=["longitude_destination", "latitude_destination"],
    #get_tilt=15,
    get_source_color=[162, 87, 114],
    get_target_color=[124, 147, 195],
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=results_df['latitude_origin'].iloc[0], longitude=results_df['longitude_origin'].iloc[0], bearing=0, pitch=100, zoom=10,)


#TOOLTIP_TEXT = {"html": "{S000} jobs <br /> Home of commuter in red; work location in green"}

r = pdk.Deck(arc_layer, initial_view_state=view_state) #, tooltip=TOOLTIP_TEXT)
st.pydeck_chart(r)