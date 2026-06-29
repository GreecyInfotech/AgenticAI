package com.bfsi.platform.tools.common;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class ToolDefinition {

    private String serverId;
    private String name;
    private String description;
    private Map<String, Object> inputSchema;

    public ToolDefinition() {}

    public ToolDefinition(String serverId, String name, String description) {
        this.serverId = serverId;
        this.name = name;
        this.description = description;
    }

    public String getServerId() { return serverId; }
    public void setServerId(String serverId) { this.serverId = serverId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Map<String, Object> getInputSchema() { return inputSchema; }
    public void setInputSchema(Map<String, Object> inputSchema) { this.inputSchema = inputSchema; }
}
