# BoozeList

## Setup

### Prerequirements

- Docker
- Docker Compose

If you want to run the code locally, you also need:

- Python 3.7
- pipenv
- librdkafa 1.2.1

To install the correct version of librdkafka on macOS run:

```
brew install librdkafka --HEAD
```

You will also need an account at https://api-portal.systembolaget.se/
and have subscribed to the API to receive an API key to use with `/services/importer`.

### Configuration

- Copy `/.env.dist` to `/.env` and set `KAFKA_ADVERTISED_HOST_NAME` to your local IP.
`localhost` won't work for communication between Docker containers, but will work for running the services locally.
- Copy each services `.env.dist` and configure the necessary variables.

### Running the application

To start the Docker environment or rebuild services:

```
docker-compose up -d --build
```

To run a service locally, `cd` into the service's directory run `pipenv shell`, `pipenv install`
and then `python main.py`.

## Create new service

Simply run `cp -r resources/skeleton services/SERVICE_NAME` to create a minimal service stub.

## Tips

### Delete topic

To manually delete a topic, run:

```
docker-compose run kafka opt/kafka/bin/kafka-topics.sh --zookeeper zookeeper:2181 --delete --topic TOPIC_NAME
```

### Reset order

To read a topic from the beginning, use:

```
consumer.assign([TopicPartition('TOPIC_NAME', partition=0, offset=OFFSET_BEGINNING)])
```
