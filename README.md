### How to use

Do a few things:
```bash
# Go to the code.
cd beltway-wifi

# You are using a virtual environment, right? Right?
source activate $VIRTUAL_ENV_NAME

# Install the reqs
pip install -r requirements.txt

# Make it go.
python story.py\
 run\
 --es_host=$ES_HOST_PORT\
 --kibana_host=$KIBANA_HOST_PORT\
 --user=$YOUR_USERNAME\
 --password=$YOUR_PASSWORD
```

THen log in to Kibana and start with the `Start Here` dashboard...  
\# TODO moar script
