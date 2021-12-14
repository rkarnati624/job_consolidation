import json
import xml

import requests

import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

from base64 import b64encode
from configparser import ConfigParser
import os

from datetime import timedelta, datetime

config = ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)


def color_survived(val):
    if val == 'ERROR':
        color = 'red'
    elif val == 'RUNNING':
        color = 'grey'
    elif val == 'ABORTED':
        color = 'pink'
    elif val == 'OK':
        color = 'black'
    elif val == 'succeeded':
        color = 'black'
    else:
        color = 'white'
    return f'background-color: {color}'


def get_token():
    client_id = r'42fb3e9a-3159-400d-8d6c-c6024942b5af'
    client_pw = r'SZ"H&M-}b"7gfc$'
    client_combined = client_id + ":" + client_pw
    # client_combined_base64_as_bytes = b64encode(str.encode(client_combined))
    client_combined_base64 = b64encode(str.encode(client_combined)).decode()

    response = requests.post('https://account.demandware.com/dw/oauth2/access_token',
                             headers={'Authorization': 'Basic %s' % client_combined_base64,
                                      "Content-Type": "application/x-www-form-urlencoded"},
                             data={'grant_type': 'client_credentials'})
    # print(response)
    json_to_python = response.json()
    return json_to_python['access_token']


def get_job_execution_search(job, scc_url):
    global token
    payload = {
        "count": 1,
        "expand": [
            "string"],
        "query": {"term_query":
                      {"fields": ["job_id"],
                       "operator": "is",
                       "values": ["%s" % job]}},
        "sorts": [
            {
                "field": "start_time",
                "sort_order": "desc"
            }
        ],
        "start": 0
    }
    payload = json.dumps(payload)
    response = requests.post(url=scc_url,
                             headers={'Authorization': 'Bearer %s' % token, "Content-Type": "application/json"},
                             data=payload, verify=False)
    job_status = response.json()
    return job_status


def jobs_status_check(jobs, scc_url, env):
    global current_date
    all_items = []
    for job in jobs:
        response1 = get_job_execution_search(job, scc_url)
        job_count = response1['count']
        for i in range(job_count):
            job_starttime = response1['hits'][i]['start_time'][:-8]
            try:
                job_endtime = response1['hits'][i]['end_time'][:-8]
                job_endtime = datetime.strptime(job_endtime, '%Y-%m-%dT%H:%M')
                job_endtime = job_endtime - timedelta(hours=8)
            except:
                job_endtime = 'RUNNING'

            job_status = response1['hits'][i]['status']
            job_name = job
            job_env = env
            project = 'scc'
            job_starttime = datetime.strptime(job_starttime, '%Y-%m-%dT%H:%M')
            job_starttime = job_starttime - timedelta(hours=8)
            store_items = [job_name, job_starttime, job_endtime, job_status, job_env, project]
            all_items.append(store_items)

    xmlToDf = pd.DataFrame(all_items, columns=[
        'job_name', 'job_starttime', 'job_endtime', 'status', 'environment', 'project'])
    sql_engine = create_engine('mysql+pymysql://jobsapp:jobsapp@ortest02.ydesigngroup.net/jobsdb')
    connection = sql_engine.connect()
    xmlToDf.to_sql('job_monitoring_log', if_exists='append', index=False, con=connection)
    return xmlToDf


def app():
    st.title("SFCC")
    global token
    token = get_token()
    code_version_response = requests.get(
        url='https://staging-web-lumens.demandware.net/s/-/dw/data/v21_10/code_versions',
        headers={'Authorization': 'Bearer %s' % token, "Content-Type": "application/json"},
        verify=False)
    resp = code_version_response.json()
    resp1 = resp["data"][19]['id']
    st.write('Current active build on staging : ' + resp1)
    Imports = ('Import Inventory Only to Demandware', 'Import PriceBooks to Demandware From Lumens FTP Site',
               'WorkFlowCatalog-Pricebook-MinMax-Index(Catalog Import) New',
               'WorkFlowWeekend-MinMax-Index New', 'partial_publish', 'Bazaarvoice Inline Rating Import')
    internal_jobs = ('GenerateNNSale_ProductIDs_Lumens', 'GenerateNNSale_ProductIDs_YLighting',
                     'Custom_NN_Sale_Lumens1',
                     'Custom_NN_Sale_Lumens2', 'Custom_NN_Sale_Lumens3', 'Custom_NN_Sale_Lumens4',
                     'Custom_NN_Sale_YLighting1', 'Custom_NN_Sale_YLighting2', 'Custom_NN_Sale_YLighting3',
                     'Custom_NN_Sale_YLighting4')
    feed_exports = ('pla_lu', 'pla_yl_0', 'pla_yl_1', 'pla_yl_2',
                    'pla_yl_3', 'Bazaarvoice Product Feed', 'Export ActiveData MarginSale Calculation',
                    'Export Catalog',
                    'Export Orders To NetSuite Lumens(OMS)',
                    'Export Orders To NetSuite YLighting(OMS)', 'Export PriceBooks',
                    'Export Trade Customers To NetSuite',
                    'Export Trade Customers To NetSuite for YL/YV')
    other_exports = ('Export Orders To NetSuite',
                     'Export Promotions',
                     'Export and Upload Adobe')

    operational_jobs = ('replication_to_prod', 'replication_to_prod_pricebooks', 'Search Index Full Lumens',
                        'Search Index Full Ylighting')
    staging_jobs = ['Bazaarvoice Inline Rating Import', 'Bazaarvoice Product Feed', 'Custom_NN_Sale_Lumens1',
                    'Custom_NN_Sale_Lumens2', 'Custom_NN_Sale_Lumens3', 'Custom_NN_Sale_Lumens4',
                    'Custom_NN_Sale_YLighting1', 'Custom_NN_Sale_YLighting2', 'Custom_NN_Sale_YLighting3',
                    'Custom_NN_Sale_YLighting4', 'pla_lu', 'pla_yl_0', 'pla_yl_1', 'pla_yl_2',
                    'pla_yl_3', 'replication_to_prod', 'replication_to_prod_pricebooks', 'Export Orders To NetSuite',
                    'Export Promotions',
                    'Export and Upload Adobe', 'GenerateNNSale_ProductIDs_Lumens',
                    'GenerateNNSale_ProductIDs_YLighting',
                    'Import Inventory Only to Demandware', 'Import PriceBooks to Demandware From Lumens FTP Site',
                    'Search Index Full Lumens', 'Search Index Full Ylighting',
                    'WorkFlowCatalog-Pricebook-MinMax-Index(Catalog Import) New',
                    'WorkFlowWeekend-MinMax-Index New', 'partial_publish']
    prod_jobs = ['	Export ActiveData MarginSale Calculation', 'Export Catalog',
                 'Export Orders To NetSuite Lumens(OMS)',
                 'Export Orders To NetSuite YLighting(OMS)', 'Export PriceBooks', 'Export Trade Customers To NetSuite',
                 'Export Trade Customers To NetSuite for YL/YV']
    staging_url = 'https://staging-web-lumens.demandware.net/s/-/dw/data/v21_10/job_execution_search'
    jobs_status_check(staging_jobs, staging_url, 'staging')
    prod_url = 'https://production-web-lumens.demandware.net/s/-/dw/data/v21_10/job_execution_search'
    jobs_status_check(prod_jobs, prod_url, 'production')
    sql_engine = create_engine('mysql+pymysql://jobsapp:jobsapp@ortest02.ydesigngroup.net/jobsdb')
    cnxn = sql_engine.connect()

    # import jobs
    scc_query_imports = """SELECT job_name, job_starttime, job_endtime,status,environment,project FROM 
    (
    SELECT job_name, job_starttime, job_endtime,status,environment,
    case when status='ERROR' THEN 1
        WHEN STATUS ='RUNNING' THEN 2
        WHEN STATUS ='OK' THEN 3 END AS PRIORITY, project
    FROM
    (
    SELECT  DISTINCT job_name, job_starttime, job_endtime,status, 
    environment, project FROM jobsdb.job_monitoring_log WHERE job_name IN {}
    ) A order by PRIORITY ASC ,job_starttime DESC
    ) B""".format(Imports)
    scc_import_df = pd.read_sql(scc_query_imports, con=cnxn)
    scc_import_df = scc_import_df.drop_duplicates(['job_name'], keep='first')

    # internal jobs
    scc_query_internal = """SELECT job_name, job_starttime, job_endtime,status,environment,project FROM 
        (
        SELECT job_name, job_starttime, job_endtime,status,environment,
        case when status='ERROR' THEN 1
            WHEN STATUS ='RUNNING' THEN 2
            WHEN STATUS ='OK' THEN 3 END AS PRIORITY, project
        FROM
        (
        SELECT  DISTINCT job_name, job_starttime, job_endtime,status, 
        environment, project FROM jobsdb.job_monitoring_log WHERE job_name IN {}
        ) A order by PRIORITY ASC ,job_starttime DESC
        ) B""".format(internal_jobs)
    scc_internal_df = pd.read_sql(scc_query_internal, con=cnxn)
    scc_internal_df = scc_internal_df.drop_duplicates(['job_name'], keep='first')

    # feed exports
    scc_query_feed = """SELECT job_name, job_starttime, job_endtime,status,environment,project FROM 
        (
        SELECT job_name, job_starttime, job_endtime,status,environment,
        case when status='ERROR' THEN 1
            WHEN STATUS ='RUNNING' THEN 2
            WHEN STATUS ='OK' THEN 3 END AS PRIORITY, project
        FROM
        (
        SELECT  DISTINCT job_name, job_starttime, job_endtime,status, 
        environment, project FROM jobsdb.job_monitoring_log WHERE job_name IN {}
        ) A order by PRIORITY ASC ,job_starttime DESC
        ) B""".format(feed_exports)
    scc_feed_df = pd.read_sql(scc_query_feed, con=cnxn)
    scc_feed_df = scc_feed_df.drop_duplicates(['job_name'], keep='first')

    # operational jobs
    scc_query_operational = """SELECT job_name, job_starttime, job_endtime,status,environment,project FROM 
        (
        SELECT job_name, job_starttime, job_endtime,status,environment,
        case when status='ERROR' THEN 1
            WHEN STATUS ='RUNNING' THEN 2
            WHEN STATUS ='OK' THEN 3 END AS PRIORITY, project
        FROM
        (
        SELECT  DISTINCT job_name, job_starttime, job_endtime,status, 
        environment, project FROM jobsdb.job_monitoring_log WHERE job_name IN {}
        ) A order by PRIORITY ASC ,job_starttime DESC
        ) B""".format(operational_jobs)
    scc_operational_df = pd.read_sql(scc_query_operational, con=cnxn)
    scc_operational_df = scc_operational_df.drop_duplicates(['job_name'], keep='first')

    col1, col2 = st.columns(2)
    with col1:
        st.header("Imports")
        st.table(scc_import_df.style.applymap(color_survived, subset=['status']))
    with col2:
        st.header("Internal")
        st.table(scc_internal_df.style.applymap(color_survived, subset=['status']))

    col1, col2 = st.columns(2)
    with col1:
        st.header("Feed Exports")
        st.table(scc_feed_df.style.applymap(color_survived, subset=['status']))
    with col2:
        st.header("Operational")
        st.table(scc_operational_df.style.applymap(color_survived, subset=['status']))
    ####################################################################

    # staging_jobs = ['Bazaarvoice Inline Rating Import', 'Bazaarvoice Product Feed', 'Custom_NN_Sale_Lumens1',
    #                 'Custom_NN_Sale_Lumens2', 'Custom_NN_Sale_Lumens3', 'Custom_NN_Sale_Lumens4',
    #                 'Custom_NN_Sale_YLighting1', 'Custom_NN_Sale_YLighting2', 'Custom_NN_Sale_YLighting3',
    #                 'Custom_NN_Sale_YLighting4', 'pla_lu', 'pla_yl_0', 'pla_yl_1', 'pla_yl_2',
    #                 'pla_yl_3', 'replication_to_prod', 'replication_to_prod_pricebooks', 'Export Orders To NetSuite',
    #                 'Export Promotions',
    #                 'Export and Upload Adobe', 'GenerateNNSale_ProductIDs_Lumens',
    #                 'GenerateNNSale_ProductIDs_YLighting',
    #                 'Import Inventory Only to Demandware', 'Import PriceBooks to Demandware From Lumens FTP Site',
    #                 'Search Index Full Lumens', 'Search Index Full Ylighting',
    #                 'WorkFlowCatalog-Pricebook-MinMax-Index(Catalog Import) New',
    #                 'WorkFlowWeekend-MinMax-Index New', 'partial_publish']
    # prod_jobs = ['	Export ActiveData MarginSale Calculation', 'Export Catalog',
    #              'Export Orders To NetSuite Lumens(OMS)',
    #              'Export Orders To NetSuite YLighting(OMS)', 'Export PriceBooks', 'Export Trade Customers To NetSuite',
    #              'Export Trade Customers To NetSuite for YL/YV']
    # staging_url = 'https://staging-web-lumens.demandware.net/s/-/dw/data/v21_10/job_execution_search'
    # scc_response = jobs_status_check(staging_jobs, staging_url, 'staging')
    # st.table(scc_response.style.applymap(color_survived, subset=['status']))
    # prod_url = 'https://production-web-lumens.demandware.net/s/-/dw/data/v21_10/job_execution_search'
    # scc_response = jobs_status_check(prod_jobs, prod_url, 'production')
    # st.table(scc_response.style.applymap(color_survived, subset=['status']))

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.header("Imports")
    #     staging_url = 'https://staging-web-lumens.demandware.net/s/-/dw/data/v21_10/job_execution_search'
    #     scc_response_import_jobs = jobs_status_check(Imports, staging_url, 'staging')
    #     st.table(scc_response_import_jobs.head(5).style.applymap(color_survived, subset=['status']))
    # with col2:
    #     st.header("Internal")
    #     st.table(scc_internal_df.head(8).style.applymap(color_survived, subset=['status']))


    st.title("RunDeck")
    projects = ['ETL', 'Feeds', 'Inventory', 'SCC-Jobs']
    for project in projects:
        authtoken = 'D2zKG0rEKBirqizj1KMapLlvwKQfx8kL'
        url = 'https://rundeck.ydesigngroup.com/api/14/project/' + project + '/executions?authtoken=' + authtoken
        response = requests.get(url, headers={"Content-Type": "application/xml"})
        string_xml = response.content
        tree = xml.etree.ElementTree.fromstring(string_xml)
        all_items = []
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
        st.subheader(project)
        sql_engine = create_engine('mysql+pymysql://jobsapp:jobsapp@ortest02.ydesigngroup.net/jobsdb')
        connection = sql_engine.connect()
        xmlToDf.to_sql('job_monitoring_log', if_exists='append', index=False, con=connection)
        trimmed_df = xmlToDf.head(5)
        st.table(trimmed_df.style.applymap(color_survived, subset=['status']))