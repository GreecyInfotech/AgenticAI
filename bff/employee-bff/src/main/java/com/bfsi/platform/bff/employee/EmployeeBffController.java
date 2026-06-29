package com.bfsi.platform.bff.employee;

import com.bfsi.platform.bff.common.client.OrchestratorClient;
import com.bfsi.platform.bff.common.dto.ChatRequest;
import com.bfsi.platform.bff.common.dto.ChatResponse;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class EmployeeBffController {

    private final OrchestratorClient orchestratorClient;
    private final RestTemplate restTemplate;
    private final String escalationAgentUrl;

    public EmployeeBffController(OrchestratorClient orchestratorClient,
                                 RestTemplate restTemplate,
                                 @Value("${bff.escalation-agent.url:http://localhost:8413}") String escalationAgentUrl) {
        this.orchestratorClient = orchestratorClient;
        this.restTemplate = restTemplate;
        this.escalationAgentUrl = escalationAgentUrl;
    }

    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(@Valid @RequestBody ChatRequest request) {
        request.getContext().putIfAbsent("persona", "EMPLOYEE");
        return ResponseEntity.ok(orchestratorClient.chat(request));
    }

    @PostMapping("/cases")
    public ResponseEntity<Map> createCase(@Valid @RequestBody ChatRequest request) {
        request.setMessage("escalate: " + request.getMessage());
        request.getContext().put("requiresEscalation", true);
        ChatResponse response = orchestratorClient.chat(request);
        return ResponseEntity.ok(Map.of(
                "requestId", response.getRequestId(),
                "status", response.getStatus(),
                "reply", response.getReply(),
                "requiresEscalation", response.isRequiresEscalation()
        ));
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("UP");
    }
}
