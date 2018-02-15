FROM python:3
MAINTAINER jghibiki <jghibiki.games@gmail.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code

# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /code
WORKDIR /code
RUN pip install -r requirements.txt
COPY . /code
RUN rm /code/custom_client.py && touch /code/custom_client.py
RUN touch /code/game_data.json
CMD ["/code/run.sh"]
