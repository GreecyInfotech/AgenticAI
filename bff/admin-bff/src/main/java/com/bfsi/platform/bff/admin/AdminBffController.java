package com.bfsi.platform.bff.admin;

import com.bfsi.platform.agents.common.registry.AgentRegistration;
import com.bfsi.platform.bff.common.client.OrchestratorClient;
import com.bfsi.platform.bff.common.dto.ChatRequest;
import com.bfsi.platform.bff.common.dto.ChatResponse;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class AdminBffController {

    private final OrchestratorClient orchestratorClient;
    private final RestTemplate restTemplate;
    private final String registryUrl;

    public AdminBffController(OrchestratorClient orchestratorClient,
                              RestTemplate restTemplate,
                              @Value("${bff.registry.url:http://localhost:8201}") String registryUrl) {
        this.orchestratorClient = orchestratorClient;
        this.restTemplate = restTemplate;
        this.registryUrl = registryUrl;
    }

    @GetMapping("/agents")
    public ResponseEntity<List<AgentRegistration>> listAgents() {
        List<AgentRegistration> agents = restTemplate.exchange(
                registryUrl + "/api/v1/registry/agents",
                HttpMethod.GET, null,
                new ParameterizedTypeReference<List<AgentRegistration>>() {}
        ).getBody();
        return ResponseEntity.ok(agents);
    }

    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(@Valid @RequestBody ChatRequest request) {
        request.getContext().putIfAbsent("persona", "ADMIN");
        return ResponseEntity.ok(orchestratorClient.chat(request));
    }

    @GetMapping("/platform/health")
    public ResponseEntity<Map<String, String>> platformHealth() {
        return ResponseEntity.ok(Map.of(
                "orchestrator", ping("http://localhost:8200/api/v1/orchestrate/health"),
                "registry", ping(registryUrl + "/api/v1/registry/agents"),
                "status", "UP"
        ));
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("UP");
    }

    private String ping(String url) {
        try {
            return restTemplate.getForObject(url, String.class) != null ? "UP" : "DOWN";
        } catch (Exception e) {
            return "DOWN";
        }
    }
}
