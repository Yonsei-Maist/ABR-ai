FROM       ubuntu:20.04
MAINTAINER arknell@yonsei.ac.kr

# update pacakge
RUN apt update
RUN apt-get update

# install python 3
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt-get install -y libgl1-mesa-glx
RUN DEBIAN_FRONTEND="noninteractive" TZ="Asia/Seoul" apt-get -y install tzdata
RUN apt-get install -y libgtk2.0-dev
RUN apt-get install -y git

# install library
RUN pip3 install tensorflow
RUN pip3 install opencv-python
RUN pip3 install flask
RUN pip3 install pymysql
RUN pip3 install flask_cors
RUN pip3 install flask_restful
RUN pip3 install matplotlib
RUN pip3 install pycryptodome==3.4.3
RUN pip3 install -U git+https://git@github.com/Yonsei-Maist/ABR-image-processor.git
RUN pip3 install -U git+https://git@github.com/Yonsei-Maist/maist-model-core.git

# copy source
COPY . /usr/src/app

# move to source
WORKDIR /usr/src/app

# start server
ENTRYPOINT python3 serve.py $AES_KEY dev
