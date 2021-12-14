import streamlit as st
import pyodbc
import pandas as pd
from sqlalchemy import create_engine


def app():
    cnxn = pyodbc.connect('Driver={SQL Server};',
                          SERVER='capimdb01.ydesigngroup.net',
                          DATABASE='LumensPIM',
                          UID='sa',
                          PWD='$QL@dm1n')
    sql_inv_job = """select TOP 3
        j.name as 'job_name',
        run_date,
        run_time,
        CASE
        WHEN run_status = '1' then 'Finished'
        ELSE 'running'
        END AS status
        From msdb.dbo.sysjobs j 
        INNER JOIN msdb.dbo.sysjobhistory h 
        ON j.job_id = h.job_id 
        where j.enabled = 1  --Only Enabled Jobs
        and j.name IN ('Update PIM Inventory')
        order by run_date desc
    """

    sql_lu_inv_job = """select TOP 3
        j.name as 'job_name',
        run_date,
        run_time,
        CASE
        WHEN run_status = '1' then 'Finished'
        ELSE 'running'
        END AS status
        From msdb.dbo.sysjobs j 
        INNER JOIN msdb.dbo.sysjobhistory h 
        ON j.job_id = h.job_id 
        where j.enabled = 1  --Only Enabled Jobs
        and j.name IN ('Update_Lumens_Inventory')
        order by run_date desc
        """
    df_pim_inv = pd.read_sql(sql_inv_job, cnxn, index_col=None, coerce_float=True, params=None, parse_dates=None,
                             columns=None,
                             chunksize=None)
    sql_engine = create_engine('mysql+pymysql://jobsapp:jobsapp@ortest02.ydesigngroup.net/jobsdb')
    connection = sql_engine.connect()
    df_pim_inv.to_sql('inv_job_monitoring_log', if_exists='append', index=False, con=connection)
    st.subheader('Inventory Job')
    st.table(df_pim_inv)
    df_LU_inv = pd.read_sql(sql_lu_inv_job, cnxn, index_col=None, coerce_float=True, params=None, parse_dates=None,
                            columns=None,
                            chunksize=None)
    st.subheader('LU Inv Job')
    st.table(df_LU_inv)

