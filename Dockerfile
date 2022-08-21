FROM python:3.8-slim-buster

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#add lib-list
COPY src/requirements.txt requirements.txt

# add app
ADD ./src /usr/src/app

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

# run server
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app", "--reload"]
#docker build --tag python-docker .
#docker run -p 5000:5000 python-docker