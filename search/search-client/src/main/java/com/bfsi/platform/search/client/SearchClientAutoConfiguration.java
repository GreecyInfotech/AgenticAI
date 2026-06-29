package com.bfsi.platform.search.client;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
@EnableConfigurationProperties(SearchClientProperties.class)
public class SearchClientAutoConfiguration {

    @Bean
    @Primary
    @ConditionalOnProperty(prefix = "search", name = "backend", havingValue = "elasticsearch")
    public SearchStore elasticsearchSearchStore(SearchClientProperties properties) {
        return new ElasticsearchSearchStore(
                properties.getHost(),
                properties.getPort(),
                properties.getIndexPrefix()
        );
    }

    @Bean
    @Primary
    @ConditionalOnProperty(prefix = "search", name = "backend", havingValue = "memory", matchIfMissing = true)
    public SearchStore inMemorySearchStore() {
        return new InMemorySearchStore();
    }
}
