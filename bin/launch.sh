cd data_loader
bash run.sh\
&& cd ../data_integrator\
&& bash run.sh \
&& cd ../data_processor\
&& bash run.sh "$1"\
&& cd ../bin \
