package com.bfsi.platform.orchestrator;

import com.bfsi.platform.agents.common.AgentRequest;
import com.bfsi.platform.agents.common.OrchestrationResult;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/orchestrate")
public class OrchestratorController {

    private final AgentOrchestratorService orchestratorService;

    public OrchestratorController(AgentOrchestratorService orchestratorService) {
        this.orchestratorService = orchestratorService;
    }

    @PostMapping
    public ResponseEntity<OrchestrationResult> orchestrate(@Valid @RequestBody AgentRequest request) {
        return ResponseEntity.ok(orchestratorService.orchestrate(request));
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("UP");
    }
}
