package com.bfsi.platform.agents.common.web;

import com.bfsi.platform.agents.common.AgentCapabilities;
import com.bfsi.platform.agents.common.AgentRequest;
import com.bfsi.platform.agents.common.AgentResponse;
import com.bfsi.platform.agents.common.BfsiAgent;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

public abstract class AgentController {

    private final BfsiAgent agent;

    protected AgentController(BfsiAgent agent) {
        this.agent = agent;
    }

    @PostMapping("/process")
    public ResponseEntity<AgentResponse> process(@Valid @RequestBody AgentRequest request) {
        return ResponseEntity.ok(agent.process(request));
    }

    @GetMapping("/capabilities")
    public ResponseEntity<AgentCapabilities> capabilities() {
        return ResponseEntity.ok(agent.getCapabilities());
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("UP");
    }
}
