# Kafka topic bootstrap (run after Kafka is up)
# Usage: kafka-topics --bootstrap-server localhost:9092 --create --if-not-exists ...

bfsi.orchestration.events    partitions=3 replication=1
bfsi.agent.decisions         partitions=3 replication=1
bfsi.audit.events            partitions=3 replication=1
bfsi.notification.events     partitions=2 replication=1
bfsi.search.index            partitions=3 replication=1
