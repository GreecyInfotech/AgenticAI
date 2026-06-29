package com.bfsi.platform.bff.customer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {"com.bfsi.platform.bff.customer", "com.bfsi.platform.bff.common"})
public class CustomerBffApplication {
    public static void main(String[] args) {
        SpringApplication.run(CustomerBffApplication.class, args);
    }
}
