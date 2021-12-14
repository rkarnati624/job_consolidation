import RunDeck
import MainPage
import Scc
import pim
import netsuite

import streamlit as st

st.set_page_config(page_title=None, page_icon=None, layout="wide")

PAGES = {
    #"MainPage": MainPage,
    "SalesForce": Scc,
    "RunDeck": RunDeck,
    #"PIM": pim,
    #"NetSuite": netsuite
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
