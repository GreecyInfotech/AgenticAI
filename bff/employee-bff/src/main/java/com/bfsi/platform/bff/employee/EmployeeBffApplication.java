package com.bfsi.platform.bff.employee;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = {"com.bfsi.platform.bff.employee", "com.bfsi.platform.bff.common"})
public class EmployeeBffApplication {
    public static void main(String[] args) {
        SpringApplication.run(EmployeeBffApplication.class, args);
    }
}
