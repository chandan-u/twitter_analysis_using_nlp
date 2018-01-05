"""
This script just defines the Airflow DAG. It's not the actual processing.
Based on the dag defined here the execution takes place in a different context
For distributed computing its advised to use XCom

more info: https://airflow.apache.org/tutorial.html#tasks


TODO: Replace print statements with logging.info in future
"""

import os

# We need this to instantiate the DAG
from airflow import DAG

# We need an operator to execute our scripts
from airflow.operators.bash_operator import BashOperator






# args/config can be varied for production/dev environments
# Its good to have default one around
from datetime import datetime, timedelta

default_args = {
    'owner': 'ChandanU',
    'depends_on_past': False,
    'start_date': datetime(2018, 01, 03),
    'email': ['chandan.uppuluri@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    #'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


# Instantiate DAG object
dag = DAG('Grabber.py', default_args=default_args)


#  directory paths
scripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','scripts')
datasets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data')
#unittests_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','tests')

# Operators sequence
task_download = BashOperator(
    task_id='download_movielens_data',
    bash_command='python ' + os.path.join(scripts_path, 'new_grabber.py'),
    dag=dag)

print("Streaming news data...")




# uncomment this if you have to remove files in the dataset dir
# except for the final transformed data

# task_rmdir_base = BashOperator(

#     task_id='rmdir_movielens_data',
#     bash_command='rm -r ' + os.path.join(datasets_path, 'ml-latest-small',''),
#     dag=dag)

# print("removing unnecessary files @dataset")






# setting up dependencies.
#task_unzip.set_upstream(task_download)
