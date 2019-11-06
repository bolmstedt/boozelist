# BoozeList

## Setup

### Prerequirements

If you want to run the code locally, install `librdkafa`. On macOS run:
```
brew install librdkafka --HEAD
```

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
