package com.bfsi.platform.tools.api;

import com.bfsi.platform.tools.client.McpHttpToolClient;
import com.bfsi.platform.tools.client.ToolDiscoveryService;
import com.bfsi.platform.tools.common.*;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class ToolController {

    private final ToolDiscoveryService discovery;
    private final McpHttpToolClient client;

    public ToolController(ToolDiscoveryService discovery, McpHttpToolClient client) {
        this.discovery = discovery;
        this.client = client;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> servers = new HashMap<>();
        discovery.serverUrls().forEach((id, url) -> servers.put(id, client.isServerHealthy(id) ? "UP" : "DOWN"));
        return ResponseEntity.ok(Map.of("status", "UP", "service", "tools-api", "servers", servers));
    }

    @GetMapping("/tools")
    public ResponseEntity<List<ToolDefinition>> listTools() {
        return ResponseEntity.ok(discovery.listAllTools());
    }

    @GetMapping("/servers")
    public ResponseEntity<List<ToolServerManifest>> listServers() {
        return ResponseEntity.ok(discovery.discoverAll());
    }

    @PostMapping("/invoke")
    public ResponseEntity<ToolInvocationResult> invoke(@Valid @RequestBody ToolInvocationRequest request) {
        ToolInvocationResult result = client.invoke(
            request.getServerId(),
            request.getToolName(),
            request.getArguments()
        );
        result.setRequestId(request.getRequestId());
        return ResponseEntity.ok(result);
    }
}
