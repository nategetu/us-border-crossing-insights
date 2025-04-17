FROM apache/airflow:2.10.5

WORKDIR /opt/airflow

USER root
COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir "apache-airflow[amazon]==${AIRFLOW_VERSION}" apache-airflow-providers-amazon==9.6.0
RUN python3 -m pip install -r /requirements.txt
USER airflow
