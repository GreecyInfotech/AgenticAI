package com.bfsi.platform.tools.client;

import com.bfsi.platform.tools.common.*;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Component
public class McpHttpToolClient implements ToolExecutor {

    private static final Logger log = LoggerFactory.getLogger(McpHttpToolClient.class);

    private final ToolClientProperties properties;
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public McpHttpToolClient(ToolClientProperties properties,
                             RestTemplate toolRestTemplate,
                             ObjectMapper objectMapper) {
        this.properties = properties;
        this.restTemplate = toolRestTemplate;
        this.objectMapper = objectMapper;
    }

    @Override
    public ToolInvocationResult invoke(String serverId, String toolName, Map<String, Object> arguments) {
        long start = System.currentTimeMillis();
        if (!properties.isEnabled()) {
            return ToolInvocationResult.failed(serverId, toolName, "Tool client disabled", 0);
        }

        String baseUrl = properties.getServers().get(serverId);
        if (baseUrl == null || baseUrl.isBlank()) {
            return ToolInvocationResult.failed(serverId, toolName, "Unknown server: " + serverId, 0);
        }

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            ResponseEntity<String> response = restTemplate.exchange(
                baseUrl + "/tools/" + toolName,
                HttpMethod.POST,
                new HttpEntity<>(arguments != null ? arguments : Map.of(), headers),
                String.class
            );

            Map<String, Object> data = parseData(response.getBody());
            return ToolInvocationResult.ok(serverId, toolName, data, System.currentTimeMillis() - start);
        } catch (Exception ex) {
            log.warn("Tool invocation failed {}.{}: {}", serverId, toolName, ex.getMessage());
            return ToolInvocationResult.failed(serverId, toolName, ex.getMessage(),
                System.currentTimeMillis() - start);
        }
    }

    public ToolServerManifest fetchManifest(String serverId) {
        String baseUrl = properties.getServers().get(serverId);
        if (baseUrl == null) {
            throw new ToolException("Unknown server: " + serverId);
        }
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(baseUrl + "/mcp/manifest", String.class);
            JsonNode root = objectMapper.readTree(response.getBody());
            ToolServerManifest manifest = new ToolServerManifest();
            manifest.setServerId(serverId);
            manifest.setName(root.path("name").asText());
            manifest.setDescription(root.path("description").asText());
            manifest.setProtocol(root.path("protocol").asText());
            manifest.setBaseUrl(baseUrl);

            List<ToolDefinition> tools = new ArrayList<>();
            root.path("tools").forEach(node -> {
                ToolDefinition def = new ToolDefinition(serverId, node.path("name").asText(), node.path("description").asText());
                def.setInputSchema(objectMapper.convertValue(node.path("inputSchema"), new TypeReference<>() {}));
                tools.add(def);
            });
            manifest.setTools(tools);
            return manifest;
        } catch (Exception e) {
            throw new ToolException("Failed to fetch manifest for " + serverId, e);
        }
    }

    public boolean isServerHealthy(String serverId) {
        String baseUrl = properties.getServers().get(serverId);
        if (baseUrl == null) return false;
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(baseUrl + "/health", String.class);
            return response.getStatusCode().is2xxSuccessful();
        } catch (Exception e) {
            return false;
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> parseData(String body) {
        try {
            JsonNode root = objectMapper.readTree(body);
            if (root.has("data")) {
                return objectMapper.convertValue(root.get("data"), new TypeReference<>() {});
            }
            return objectMapper.convertValue(root, new TypeReference<>() {});
        } catch (Exception e) {
            return Map.of("raw", body);
        }
    }
}
