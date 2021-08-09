[root@vj-oci-docker Todo-List-Dockerized-Flask-WebApp]# cat Dockerfile
# build the image based on python:3.8-slim-buster image
#FROM python:3.8-slim-buster
FROM oraclelinux:7-slim

RUN yum -y install oraclelinux-developer-release-el7 oracle-instantclient-release-el7 && \
    yum -y install python3 \
                   python3-libs \
                   python3-pip \
                   python3-setuptools \
                   python36-cx_Oracle && \
    rm -rf /var/cache/yum/*



# metadata in the form of key=value about the maintainer of the image
LABEL Maintainer_Name="Vijay Balebail" Maintainer_Email="vbalebai@gmail.com"

# the work directory inside the container
WORKDIR /

# set enviournment variables
ENV FLASK_APP app.py
ENV FLASK_ENV development

# copy the requirements file inside the container
COPY ./requirements.txt /requirements.txt

# install the requirements using pip3
RUN pip3 install -r requirements.txt

RUN mkdir app
WORKDIR /app

# copy the project artefects into the container under the root directory
COPY . .

# the command to run once we run the container
CMD python3 app.py
