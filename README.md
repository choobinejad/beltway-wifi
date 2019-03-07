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
 --password=$YOUR_PASSWORD\
 --new_users_password=$NEW_USERS_PASSWORD\
 --speed=8\
 --verify_certs=True
```

- `es_host`: e.g. `https://localhost:9200`  
- `kibana_host`: e.g. `https://localhost:5601`  
- `user`: an initial superuser e.g. `elastic`  
- `password`: the initial user's password  
- `new_users_password`: this demo generated some users (`analyst`, `developer`, and `tech-partner`). This will be the password for each.  
- `speed`: int, 1-n. At the default (`8`), the demo generated about 1.5gb of `network_events` per day.  
- `run_seconds`: optional, int, seconds. For running demo feeds for a specified period of time.
- `verify_certs`: bool, `True` or `False`. Whether to verify ES server certs when setting up the ES client.  


Then log in to Kibana and start with the `Start Here` dashboard.

