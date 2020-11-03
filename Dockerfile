FROM       ubuntu:20.04
MAINTAINER arknell@yonsei.ac.kr

# update pacakge
RUN apt update

# install python 3.8
RUN apt install -y python3

# install library
RUN pip install tensorflow
RUN pip install opencv-python
RUN pip install flask

# copy source
COPY . /usr/src/app

# move to source
WORKDIR /usr/src/app

# start server
EXPOSE 9000
CMD    nohup python3 serve.py > log 2>&1 &
