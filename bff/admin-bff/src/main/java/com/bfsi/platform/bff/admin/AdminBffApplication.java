package com.bfsi.platform.bff.admin;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {"com.bfsi.platform.bff.admin", "com.bfsi.platform.bff.common"})
public class AdminBffApplication {
    public static void main(String[] args) {
        SpringApplication.run(AdminBffApplication.class, args);
    }
}
