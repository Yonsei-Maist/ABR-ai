FROM       ubuntu:20.04
MAINTAINER arknell@yonsei.ac.kr

# update pacakge
RUN apt update

# install python 3
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install git

# install library
RUN pip3 install tensorflow
RUN pip3 install opencv-python
RUN pip3 install flask
RUN pip3 install -U git+https://git@github.com/Yonsei-Maist/ABR-image-processor.git

# copy source
COPY . /usr/src/app

# move to source
WORKDIR /usr/src/app

# start server
ENTRYPOINT ["python"]
CMD ["serve.py"]
