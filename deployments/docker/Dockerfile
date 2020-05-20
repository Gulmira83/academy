## Building the docker container based on python
FROM python

## Copying all django app to docker container 
COPY ./academy /website

## Changing the workspace
WORKDIR /website

## Putting inside Docker file which environment is 
ARG branch_name
ENV ENVIRONMENT=$branch_name

## Installing all libraries 
RUN pip install -r requirements.txt

## Expose the port for the webapp
EXPOSE 5000

## Making sure that application will run on first start 
CMD [ "/bin/sh", "-c", "sleep 10 && python manage.py migrate --run-syncdb && python manage.py runserver 0.0.0.0:5000 --insecure"]