FROM python:3.7-alpine
ARG SERVICE_NAME

RUN apk upgrade --update-cache --available \
    && apk add --no-cache build-base \
    && apk add --no-cache --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community librdkafka librdkafka-dev
RUN pip3 install pipenv

COPY services/$SERVICE_NAME/Pipfile* /tmp/python/install/
COPY packages /tmp/packages
RUN cd /tmp/python/install \
    && pipenv lock --three --requirements | sed "s/^-e //" > requirements.txt \
    && pip install -r requirements.txt

WORKDIR /app
COPY services/$SERVICE_NAME/app ./app
COPY services/$SERVICE_NAME/main.py ./

CMD [ "python", "-u", "./main.py" ]
