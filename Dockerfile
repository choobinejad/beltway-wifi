FROM python:3.7.2-alpine3.9

WORKDIR /usr/src/app

COPY ./src/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY ./src .

ENTRYPOINT [ "python" ]
CMD [ "./story.py", "run", " --es_host=$ES_HOST", " --kibana_host=$KIBANA_HOST", " --user=$USER", " --password=$PASSWORD", " --new_users_password=$NEW_USERS_PASSWORD", "--speed=8", "verify_certs=$VERIFY_CERTS" ]
