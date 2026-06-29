package com.bfsi.platform.rag.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration
@ConditionalOnProperty(prefix = "rag.vector", name = "store", havingValue = "pgvector")
@Import(DataSourceAutoConfiguration.class)
public class PgVectorDataSourceConfig {
}
