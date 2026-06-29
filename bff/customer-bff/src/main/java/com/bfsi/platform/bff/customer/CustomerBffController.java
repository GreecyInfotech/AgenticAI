package com.bfsi.platform.bff.customer;

import com.bfsi.platform.bff.common.client.OrchestratorClient;
import com.bfsi.platform.bff.common.dto.ChatRequest;
import com.bfsi.platform.bff.common.dto.ChatResponse;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1")
public class CustomerBffController {

    private final OrchestratorClient orchestratorClient;

    public CustomerBffController(OrchestratorClient orchestratorClient) {
        this.orchestratorClient = orchestratorClient;
    }

    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(@Valid @RequestBody ChatRequest request) {
        return ResponseEntity.ok(orchestratorClient.chat(request));
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("UP");
    }
}
