package com.bfsi.platform.aigateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication(scanBasePackages = "com.bfsi.platform.aigateway")
@ConfigurationPropertiesScan("com.bfsi.platform.aigateway")
public class AiGatewayApplication {
  public static void main(String[] args) {
    SpringApplication.run(AiGatewayApplication.class, args);
  }
}
