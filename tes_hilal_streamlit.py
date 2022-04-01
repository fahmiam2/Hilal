from functools import cache
import streamlit as st
import ephem
import pandas as pd 
import numpy as np 
from datetime import datetime
from datetime import timedelta
# from geopy.exc import GeocoderTimedOut
# from geopy.geocoders import Nominatim

def observer(lokasi, latitude, longitude, date):
    obs = ephem.Observer()
    obs.lat = latitude
    obs.lon = longitude
    obs.date = date #waktu pengamatan hilal: YYYY/MM/DD HH:MM:SS (waktu maghrib di lokasi dalam utc) 
    #obs.date = ephem.localtime(obs.date) #convert utc ke waktu lokal
    st.text("Pengamatan hilal dilakukan pada {} WIB".format(ephem.localtime(obs.date)))
    
    # Sun-Moon Elongation and its Altitude
    Moon = ephem.Moon()
    Moon.compute(obs)
    st.text("\nKetinggian bulan pada {} WIB sebesar {} derajat \n"
        "dan elongasi bulan sebesar {} derajat".format(ephem.localtime(obs.date), Moon.alt, Moon.elong))
    
    # New Moon
    b = date.split(' ', 1)
    b = b[0]
    d = ephem.next_new_moon(b)
    #d = ephem.to_timezone(d, ephem.UTC)
    d = ephem.localtime(d)
    st.text("\nWaktu ijtimak terjadi pada: {} WIB".format(d))
    
    # Age of the Moon when does hilal observation
    d_obs = ephem.Date(obs.date)
    #d_obs = ephem.to_timezone(d_obs, ephem.UTC)
    d_obs = ephem.localtime(d_obs)
    age = d_obs - d 
    st.text("Bulan pada saat pengamatan berumur {}".format(age))
        
    # MABIMS Criteria
    alt_mabims = ephem.degrees('3:00:00')
    elong_mabims = ephem.degrees('6:24:00')
    age_mabims = timedelta(hours=8)

    if Moon.alt >= alt_mabims:
        if Moon.elong >= elong_mabims:
            if age >= age_mabims:    
                return st.markdown("\n###### Diperkirakan akan terlihat hilal di {} #######".format(lokasi))
            else:
                return st.markdown("\n####### Diperkirakan hilal tidak akan terlihat hilal di {} #######".format(lokasi))
        else:
            return st.markdown("\n####### Diperkirakan hilal tidak akan terlihat hilal di {} #######".format(lokasi))
    else:
        return st.markdown("\n####### Diperkirakan hilal tidak akan terlihat hilal di {} #######".format(lokasi))

    return

def main():
    #Title of webapp
    st.title("Prediksi hilal di Indonesia berdasarkan kriteria MABIMS")
    #Take location input
    location = st.text_input("Masukkan lokasi kota anda")

    #Take latitude input
    lat = st.text_input("Masukkan kordinat latitude anda")

    #take longitude input
    long = st.text_input("Masukkan koordinat longitude anda")

    #Take date observation of hilal
    datetime = st.text_input("Masukkan tanggal dan waktu pengamatan hilal dengan format YYYY-MM-DD HH:MM:SS UTC")
    
    if st.button("predict"):
        return observer(lokasi=location, latitude=lat, longitude=long, date=datetime)

if __name__ == "__main__":
    main()
