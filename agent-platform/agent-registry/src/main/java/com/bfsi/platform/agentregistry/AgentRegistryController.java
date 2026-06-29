package com.bfsi.platform.agentregistry;

import com.bfsi.platform.agents.common.AgentType;
import com.bfsi.platform.agents.common.registry.AgentRegistration;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/registry")
public class AgentRegistryController {

    private final AgentRegistryService registryService;

    public AgentRegistryController(AgentRegistryService registryService) {
        this.registryService = registryService;
    }

    @GetMapping("/agents")
    public ResponseEntity<List<AgentRegistration>> listAgents() {
        return ResponseEntity.ok(registryService.listAll());
    }

    @GetMapping("/agents/{type}")
    public ResponseEntity<AgentRegistration> getAgent(@PathVariable AgentType type) {
        return registryService.find(type)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
