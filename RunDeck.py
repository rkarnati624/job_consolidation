import xml
import requests
import streamlit as st
import xml.etree.ElementTree as ETree
import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta, datetime


def color_survived(val):
    color = 'red' if val == 'failed' else 'green'
    return f'background-color: {color}'


def app():
    st.title("RunDeck")
    etl_jobs_uuid = ['9a307a7b-5047-4be2-8f16-c3c4b7c0f0e9', 'efb2b1c5-f0bf-42cd-b7f2-ec80a79f3fbc']
    feeds_uuid = ['6d84b95f-e585-4182-a05e-da5aeaadaffb', '5243496e-15e8-46fd-8b7b-c83f6fd873f9',
                  '7b87fcdd-a8d9-49db-bddc-d796bd3d963f', '9cafbdec-3d4a-4c6e-a681-6bdb16dcc48e']
    # inventory_uuid = ['ed02ba9e-f75b-438d-992e-af2c88e9fd3e', 'dac42fb5-fb2f-4cd3-bed6-1b021216dfdc',
    #                   '11afe0c2-33ff-4942-93ba-5e43ed2398cd', '07bac94a-1560-439e-8fab-1537de9ffa2a',
    #                   '8a860ee6-1748-4adf-8e9f-1670f7749396']
    invoca_uuid = ['f25a23fc-1513-46df-9fbd-75353f15d46c', 'e054b807-a064-4f96-b996-9ed2992dc679',
                   'aef74ad2-32ba-409e-9274-c25e7479332d', 'c3e6aed6-a9c3-4736-a7a7-8229da015320',
                   'c7b61905-85f4-4c3b-88f7-1446086c4da9']
    scc_uuid = ['67380c93-aaf0-4cdf-a227-5e9f71e003fc', 'fc117f59-4b49-47ca-969f-9d511c24e40d',
                'ecdfd52e-a083-47f7-88f5-56bdd11ef9ef', 'b06907b9-7c04-408b-89ad-c1b11feda56f',
                '7a1b7f3b-fa2e-487c-9700-15ace138c5b', '146744e7-6a32-460b-b729-f9688d48687a']
    tableau_uuid = ['ab526c38-1a01-47f5-8e80-d1ad725013ab', 'e811d09b-5ccd-48c3-8750-91e394a950e5',
                    'a93c8596-a76f-4a64-837a-31ad4c7ad722', 'ef8f20d3-f643-4f7f-8bfd-8286b9453677',
                    '1b863189-c113-4419-a483-3ad2172c550c', 'f2b8436d-ea9e-41a0-b820-ab3070f46f9c',
                    'fb2ae761-b04c-472b-977e-4037000be47f']
    market_place_uuid = ['0777afa4-a520-4b20-9637-7dfaae12f1e6', '22fff960-b07c-459d-8076-08e4af499a51']

    projects = ['ETL', 'Feeds', 'Inventory', 'SCC-Jobs']
    all_uuid_list = etl_jobs_uuid + feeds_uuid
                    #+ inventory_uuid + invoca_uuid + scc_uuid + tableau_uuid + market_place_uuid
    #for project in projects:
    all_items = []
    for uuid in all_uuid_list:
        authtoken = 'D2zKG0rEKBirqizj1KMapLlvwKQfx8kL'
        #url = 'https://rundeck.ydesigngroup.com/api/14/project/' + project + '/executions?authtoken=' + authtoken
        job_execution_url = 'https://rundeck.ydesigngroup.com/api/11/job/'+uuid+'/executions?authtoken=' + authtoken
        response = requests.get(job_execution_url, headers={"Content-Type": "application/json"})
        string_xml = response.content
        tree = xml.etree.ElementTree.fromstring(string_xml)

        for executions in tree.iter('execution'):
            job_starttime = executions.find('date-started').text
            job_starttime = job_starttime[:-4]
            job_starttime = datetime.strptime(job_starttime, '%Y-%m-%dT%H:%M')
            job_starttime = job_starttime - timedelta(hours=8)
            job_endtime = executions.find('date-ended').text
            job_endtime = job_endtime[:-4]
            job_endtime = datetime.strptime(job_endtime, '%Y-%m-%dT%H:%M')
            job_endtime = job_endtime - timedelta(hours=8)
            job_name = executions.find('job').find('name').text
            environment = executions.find('job').find('group').text
            project = executions.find('job').find('project').text
            status = executions.attrib.get('status')
            store_items = [job_name, job_starttime, job_endtime, status, environment, project]
            all_items.append(store_items)

    xmlToDf = pd.DataFrame(all_items, columns=[
        'job_name', 'job_starttime', 'job_endtime', 'status', 'environment', 'project'])

    # Job_Name = xmlToDf['JobName'].drop_duplicates()
    # st.sidebar.header("Please Filter Here")
    # Job_Choice = st.sidebar.selectbox('Select Job Name:', Job_Name)
    # Job_Status = xmlToDf['JobStatus'].drop_duplicates()
    # Job_Status_Choice = st.sidebar.selectbox('Select Job Status:', Job_Status)
    # Project_Filter = xmlToDf['Project'].drop_duplicates()
    # Project_Filter_Choice = st.sidebar.selectbox('Select Project:', Project_Filter)
    # st.sidebar.multiselect("Please Filter Here", options=Job_Name, default=Job_Name)
    # df_selection = xmlToDf.query("JobName==@Job_Choice & JobStatus==@Job_Status_Choice & "
    #                              "Project==@Project_Filter_Choice")
    # st.table(df_selection.style.applymap(color_survived, subset=['JobStatus']))
    #st.subheader(project)
    #sql_engine = create_engine('mysql+pymysql://jobsapp:jobsapp@ortest02.ydesigngroup.net/jobsdb')
    #connection = sql_engine.connect()
    #xmlToDf.to_sql('job_monitoring_log', if_exists='append', index=False, con=connection)
    trimmed_df = xmlToDf.drop_duplicates(['job_name'], keep='first')
    st.table(trimmed_df.style.applymap(color_survived, subset=['status']))




    # authtoken = 'D2zKG0rEKBirqizj1KMapLlvwKQfx8kL'
    # job_execution_url = 'https://rundeck.ydesigngroup.com/api/11/job/9a307a7b-5047-4be2-8f16-c3c4b7c0f0e9/executions?authtoken=' + authtoken
    # response = requests.get(job_execution_url, headers={"Content-Type": "application/json"})
    # st.write(response)
    # string_xml = response.content
    # tree = xml.etree.ElementTree.fromstring(string_xml)
    # all_items = []
    # for executions in tree.iter('execution'):
    #     job_starttime = executions.find('date-started').text
    #     job_starttime = job_starttime[:-4]
    #     job_starttime = datetime.strptime(job_starttime, '%Y-%m-%dT%H:%M')
    #     st.write(job_starttime)
