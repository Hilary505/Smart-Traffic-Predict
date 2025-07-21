FROM python:3.7-stretch

####
##  Create app directory
### 

WORKDIR /usr/src/app

####
## Copy project to WORKDIR
####
COPY . ./

####
## Install app dependencies
####

RUN pip install -r requirements.txt

ARG NSW_API_KEY
ENV NSW_API_KEY=${NSW_API_KEY}

EXPOSE 5000
####
## Run python script
####

ENTRYPOINT ["python"]

CMD [ "run.py"]

####--------------------------------


