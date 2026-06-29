package com.bfsi.platform.tools.common;

import java.util.ArrayList;
import java.util.List;

public class ToolServerManifest {

    private String serverId;
    private String name;
    private String description;
    private String protocol;
    private String baseUrl;
    private List<ToolDefinition> tools = new ArrayList<>();

    public String getServerId() { return serverId; }
    public void setServerId(String serverId) { this.serverId = serverId; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getProtocol() { return protocol; }
    public void setProtocol(String protocol) { this.protocol = protocol; }
    public String getBaseUrl() { return baseUrl; }
    public void setBaseUrl(String baseUrl) { this.baseUrl = baseUrl; }
    public List<ToolDefinition> getTools() { return tools; }
    public void setTools(List<ToolDefinition> tools) {
        this.tools = tools != null ? tools : new ArrayList<>();
    }
}
