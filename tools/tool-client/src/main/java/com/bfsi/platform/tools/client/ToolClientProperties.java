package com.bfsi.platform.tools.client;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.HashMap;
import java.util.Map;

@ConfigurationProperties(prefix = "tools.mcp")
public class ToolClientProperties {

    private boolean enabled = true;
    private int timeoutSeconds = 15;
    private Map<String, String> servers = defaultServers();

    public boolean isEnabled() { return enabled; }
    public void setEnabled(boolean enabled) { this.enabled = enabled; }
    public int getTimeoutSeconds() { return timeoutSeconds; }
    public void setTimeoutSeconds(int timeoutSeconds) { this.timeoutSeconds = timeoutSeconds; }
    public Map<String, String> getServers() { return servers; }
    public void setServers(Map<String, String> servers) {
        this.servers = servers != null ? servers : defaultServers();
    }

    private static Map<String, String> defaultServers() {
        Map<String, String> map = new HashMap<>();
        map.put("core-banking", "http://localhost:8501");
        map.put("crm", "http://localhost:8502");
        map.put("postgres", "http://localhost:8503");
        map.put("regulatory", "http://localhost:8504");
        map.put("email", "http://localhost:8505");
        map.put("jira", "http://localhost:8506");
        return map;
    }
}
