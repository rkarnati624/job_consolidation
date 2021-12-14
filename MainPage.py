import streamlit as st
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ETree
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt


def app():
    st.title("Summary Dashboard")
    labels = 'Failed', 'Success', 'Running'
    sizes = [10, 60, 30]
    explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)
