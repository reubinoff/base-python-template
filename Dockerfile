FROM python:3.7.6 as base

RUN mkdir /app

# prepare env
COPY requirements.txt /app
COPY setup.py /app
COPY ./omdbweather /app/omdbweather

## Installation
WORKDIR /app 
RUN pip install -r requirements.txt
RUN python setup.py install

WORKDIR /app

CMD ["python", "-m", "omdbweather"]
