#!/usr/bin/env python3
"""Scaffold agent module boilerplate files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AGENTS = [
    ("intent", 8401, "Intent"),
    ("customer", 8402, "Customer"),
    ("kyc", 8403, "Kyc"),
    ("aml", 8404, "Aml"),
    ("fraud", 8405, "Fraud"),
    ("loan", 8406, "Loan"),
    ("underwriting", 8407, "Underwriting"),
    ("claim", 8408, "Claim"),
    ("compliance", 8409, "Compliance"),
    ("audit", 8410, "Audit"),
    ("recommendation", 8411, "Recommendation"),
    ("portfolio", 8412, "Portfolio"),
    ("escalation", 8413, "Escalation"),
    ("notification", 8414, "Notification"),
]

POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>com.bfsi.platform</groupId>
        <artifactId>bfsi-agentic-ai-platform</artifactId>
        <version>0.1.0-SNAPSHOT</version>
        <relativePath>../../pom.xml</relativePath>
    </parent>
    <artifactId>{artifact}</artifactId>
    <name>{cls} Agent</name>
    <dependencies>
        <dependency>
            <groupId>com.bfsi.platform</groupId>
            <artifactId>agent-common</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""

APP = """package {pkg};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class {cls}AgentApplication {{
    public static void main(String[] args) {{
        SpringApplication.run({cls}AgentApplication.class, args);
    }}
}}
"""

YML = """server:
  port: {port}
spring:
  application:
    name: {artifact}
management:
  endpoints:
    web:
      exposure:
        include: health,info
"""

CONTROLLER = """package {pkg};

import com.bfsi.platform.agents.common.web.AgentController;
import {pkg}.service.{cls}AgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class {cls}AgentController extends AgentController {{
    public {cls}AgentController({cls}AgentService service) {{
        super(service);
    }}
}}
"""

for name, port, cls in AGENTS:
    artifact = f"{name}-agent"
    pkg = f"com.bfsi.platform.agents.{name}"
    base = ROOT / "agents" / artifact
    java_dir = base / "src" / "main" / "java" / pkg.replace(".", "/")
    java_dir.mkdir(parents=True, exist_ok=True)
    (base / "src" / "main" / "resources").mkdir(parents=True, exist_ok=True)

    (base / "pom.xml").write_text(POM.format(artifact=artifact, cls=cls), encoding="utf-8")
    (java_dir / f"{cls}AgentApplication.java").write_text(APP.format(pkg=pkg, cls=cls), encoding="utf-8")
    (base / "src" / "main" / "resources" / "application.yml").write_text(
        YML.format(port=port, artifact=artifact), encoding="utf-8"
    )
    service_dir = java_dir / "service"
    service_dir.mkdir(exist_ok=True)
    (java_dir / f"{cls}AgentController.java").write_text(CONTROLLER.format(pkg=pkg, cls=cls), encoding="utf-8")

print(f"Scaffolded {len(AGENTS)} agents")
