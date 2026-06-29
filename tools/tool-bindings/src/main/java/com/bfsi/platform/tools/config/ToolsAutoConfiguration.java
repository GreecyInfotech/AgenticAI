package com.bfsi.platform.tools.config;

import com.bfsi.platform.tools.client.ToolClientConfig;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Import;

@AutoConfiguration
@Import(ToolClientConfig.class)
@ComponentScan(basePackages = "com.bfsi.platform.tools")
public class ToolsAutoConfiguration {
}
