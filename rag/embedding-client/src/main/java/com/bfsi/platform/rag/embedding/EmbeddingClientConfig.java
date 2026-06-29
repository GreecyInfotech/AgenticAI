package com.bfsi.platform.rag.embedding;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
@EnableConfigurationProperties(EmbeddingClientProperties.class)
public class EmbeddingClientConfig {

    @Bean
    RestTemplate embeddingRestTemplate(RestTemplateBuilder builder, EmbeddingClientProperties props) {
        return builder
            .setConnectTimeout(Duration.ofSeconds(props.getTimeoutSeconds()))
            .setReadTimeout(Duration.ofSeconds(props.getTimeoutSeconds()))
            .build();
    }

    @Bean
    ObjectMapper ragObjectMapper() {
        return new ObjectMapper();
    }
}
