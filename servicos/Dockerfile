FROM python:latest
# --- 
RUN pip3 install flask
RUN pip3 install psycopg[binary]
RUN pip3 install flask-cors
# --- 
RUN pip3 install psycopg-pool httpx requests
# ---
RUN mkdir /servico
WORKDIR /servico