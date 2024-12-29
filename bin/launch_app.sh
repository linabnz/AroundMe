#!/bin/bash
echo "Downloading data"
cd data_loader
bash run.sh \
&& cd ../data_integrator \
&& bash run.sh \
&& cd .. 
streamlit run webapp/app.py --server.port=5002 
