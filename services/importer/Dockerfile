FROM python:3.7-alpine

RUN apk upgrade --update-cache --available \
    && apk add --no-cache build-base \
    && apk add --no-cache --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community librdkafka librdkafka-dev
RUN pip3 install pipenv

COPY services/importer/Pipfile* /tmp/python/install/
COPY packages /tmp/packages
RUN cd /tmp/python/install \
    && pipenv lock --three --requirements | sed "s/^-e //" > requirements.txt \
    && pip install -r requirements.txt

WORKDIR /app
COPY services/importer/app ./app
COPY services/importer/main.py ./

CMD [ "python", "-u", "./main.py" ]
