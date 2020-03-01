import airflow
from datetime import datetime, timedelta
from airflow.operators.hive_operator import HiveOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

tmpl_search_path='/home/cloudera/'
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(7),
    'provide_context': True,
    'depends_on_past': False
}

dag = airflow.DAG(
    'process_hive_dwh',
    schedule_interval="@daily",
    dagrun_timeout=timedelta(minutes=60),
 template_searchpath=tmpl_search_path,
    default_args=args,
    max_active_runs=10)

hivestep = HiveOperator(
    hql='leftantijoin.hql',
    hiveconf_jinja_translate=True,
    #hive_cli_conn_id='hive_staging',
    schema='retail_db',
    task_id='hive_step1',
    dag=dag)

bashoperator=BashOperator(
    task_id='unixcmd',
    depends_on_past=False,
    bash_command='sh /home/cloudera/exec_hive.sh ' ,
    retries=3,
    dag=dag,
)

dummy = DummyOperator(
    task_id='dummy',
    dag=dag)


def hello(ds,**kwargs):
  return 'Hello '+ds

pytstep=PythonOperator(
    task_id='pythoncmd',
    provide_context=True,
    python_callable=hello,
    #op_args=['one', 'two', 'three'],
    dag=dag,
)


scalasparksubmit=SparkSubmitOperator(
conn_id='spark_default',
task_id='spark-submit-scala',
java_class='SparkHiveApp',
application='/home/cloudera/IdeaProjects/SparkHive/target/scala-2.11/sparkhive_2.11-0.1.jar',
verbose=True,
dag=dag,
)
hivestep >> bashoperator >> scalasparksubmit >> dummy

#if __name__ == "__main__":
#    dag.cli()
