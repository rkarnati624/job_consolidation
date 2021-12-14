import streamlit as st
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ETree
import pandas as pd
import plotly.express as px



def color_survived(val):
    color = 'red' if val=='failed' else 'green'
    return f'background-color: {color}'


st.set_page_config(page_title="dashboard",page_icon=":bar_chart:",layout="wide")
st.title("Job Monitoring Dashboard")

xmldata = "C:\\Users\\rkarnati\\Downloads\\test.xml" ##This needs to be changed as as per rest api calls
prstree = ETree.parse(xmldata)
root = prstree.getroot()
# print(root)
store_items = []
all_items = []
for executions in root.iter('execution'):
    StartDate = executions.find('date-started').text
    StartDate = pd.to_datetime(StartDate).strftime('%Y-%m-%d %H:%M:%S')
    EndDate = executions.find('date-ended').text
    EndDate = pd.to_datetime(EndDate).strftime('%Y-%m-%d %H:%M:%S')
    JobName = executions.find('job').find('name').text
    Group = executions.find('job').find('group').text
    Project = executions.find('job').find('project').text
    Status = executions.attrib.get('status')
    store_items = [JobName,StartDate,EndDate,Group,Project,Status]
    all_items.append(store_items)

xmlToDf = pd.DataFrame(all_items, columns=[
   'JobName','StartDate','EndDate','Group','Project','JobStatus'])


st.sidebar.header("Please Filter Here")
Job_Name = xmlToDf['JobName'].drop_duplicates()
Job_Choice = st.sidebar.selectbox('Select Job Name:', Job_Name)

Job_Status = xmlToDf['JobStatus'].drop_duplicates()
Job_Status_Choice = st.sidebar.selectbox('Select Job Status:', Job_Status)

Project_Filter = xmlToDf['Project'].drop_duplicates()
Project_Filter_Choice = st.sidebar.selectbox('Select Project:', Project_Filter)

df_selection=xmlToDf.query("JobName==@Job_Choice & JobStatus==@Job_Status_Choice")
st.table(df_selection.style.applymap(color_survived,subset=['JobStatus']))