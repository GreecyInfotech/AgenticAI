#!/usr/bin/env sh
# Create Kafka topics for the distributor ordering platform.
set -eu

BOOTSTRAP="${KAFKA_BOOTSTRAP_SERVERS:-localhost:9092}"

topics="
order.created
order.updated
order.cancelled
inventory.checked
inventory.reserved
promotion.applied
credit.checked
payment.completed
shipment.created
notification.sent
"

for topic in $topics; do
  echo "Creating topic: $topic"
  kafka-topics --bootstrap-server "$BOOTSTRAP" \
    --create --if-not-exists \
    --topic "$topic" \
    --partitions 3 \
    --replication-factor 1
done

echo "All topics created."
