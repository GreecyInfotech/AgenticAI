package com.bfsi.platform.tools.client;

import com.bfsi.platform.tools.common.ToolDefinition;
import com.bfsi.platform.tools.common.ToolServerManifest;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class ToolDiscoveryService {

    private final McpHttpToolClient client;
    private final ToolClientProperties properties;

    public ToolDiscoveryService(McpHttpToolClient client, ToolClientProperties properties) {
        this.client = client;
        this.properties = properties;
    }

    public List<ToolServerManifest> discoverAll() {
        List<ToolServerManifest> manifests = new ArrayList<>();
        for (String serverId : properties.getServers().keySet()) {
            try {
                manifests.add(client.fetchManifest(serverId));
            } catch (Exception ignored) {
                ToolServerManifest offline = new ToolServerManifest();
                offline.setServerId(serverId);
                offline.setName(serverId);
                offline.setDescription("Server unavailable");
                offline.setBaseUrl(properties.getServers().get(serverId));
                manifests.add(offline);
            }
        }
        return manifests;
    }

    public List<ToolDefinition> listAllTools() {
        List<ToolDefinition> tools = new ArrayList<>();
        for (ToolServerManifest manifest : discoverAll()) {
            tools.addAll(manifest.getTools());
        }
        return tools;
    }

    public Map<String, String> serverUrls() {
        return properties.getServers();
    }
}
