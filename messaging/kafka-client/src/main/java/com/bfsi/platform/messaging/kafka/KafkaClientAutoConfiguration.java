package com.bfsi.platform.messaging.kafka;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.*;

import java.util.HashMap;
import java.util.Map;

@Configuration
@EnableConfigurationProperties(KafkaClientProperties.class)
public class KafkaClientAutoConfiguration {

    @Bean
    @ConditionalOnProperty(prefix = "messaging.kafka", name = "enabled", havingValue = "true")
    public ProducerFactory<String, String> producerFactory(KafkaClientProperties properties) {
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, properties.getBootstrapServers());
        config.put(ProducerConfig.CLIENT_ID_CONFIG, properties.getClientId());
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.ACKS_CONFIG, "all");
        config.put(ProducerConfig.RETRIES_CONFIG, properties.getRetries());
        return new DefaultKafkaProducerFactory<>(config);
    }

    @Bean
    @ConditionalOnProperty(prefix = "messaging.kafka", name = "enabled", havingValue = "true")
    public KafkaTemplate<String, String> kafkaTemplate(ProducerFactory<String, String> producerFactory) {
        return new KafkaTemplate<>(producerFactory);
    }

    @Bean
    @ConditionalOnProperty(prefix = "messaging.kafka", name = "enabled", havingValue = "true")
    public ConsumerFactory<String, String> consumerFactory(KafkaClientProperties properties) {
        Map<String, Object> config = new HashMap<>();
        config.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, properties.getBootstrapServers());
        config.put(ConsumerConfig.GROUP_ID_CONFIG, properties.getConsumerGroup());
        config.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        config.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        config.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        return new DefaultKafkaConsumerFactory<>(config);
    }

    @Bean
    @ConditionalOnProperty(prefix = "messaging.kafka", name = "enabled", havingValue = "true")
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory(
            ConsumerFactory<String, String> consumerFactory) {
        ConcurrentKafkaListenerContainerFactory<String, String> factory =
                new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        return factory;
    }

    @Bean
    @ConditionalOnProperty(prefix = "messaging.kafka", name = "enabled", havingValue = "true")
    public EventPublisher kafkaEventPublisher(KafkaTemplate<String, String> kafkaTemplate) {
        ObjectMapper mapper = messagingObjectMapper();
        return new KafkaEventPublisher(kafkaTemplate, mapper);
    }

    @Bean
    @ConditionalOnProperty(prefix = "messaging.kafka", name = "enabled", havingValue = "false", matchIfMissing = true)
    public EventPublisher noOpEventPublisher() {
        return new NoOpEventPublisher();
    }

    @Bean
    public ObjectMapper messagingObjectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        return mapper;
    }
}
