package com.bfsi.platform.observability;

import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.actuate.autoconfigure.metrics.MeterRegistryCustomizer;
import org.springframework.context.annotation.Bean;

@AutoConfiguration
@ConditionalOnClass(MeterRegistry.class)
public class PlatformObservabilityAutoConfiguration {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> platformMetricsCustomizer(
            @Value("${spring.application.name:unknown}") String applicationName) {
        return registry -> registry.config()
                .commonTags("application", applicationName, "platform", "bfsi");
    }
}
