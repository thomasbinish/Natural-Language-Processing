# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image

FROM python:3.5

RUN apt-get update

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container

RUN pip install --upgrade pip

RUN mkdir /dtlk-language-core

# Set the working directory to /dltk-language-core

WORKDIR /dtlk-language-core

# Copy the current directory contents into the container at /dltk-language-core

ADD . /dtlk-language-core/

# Install any needed packages specified in requirements.txt

RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

RUN python nltk_downloads.py
