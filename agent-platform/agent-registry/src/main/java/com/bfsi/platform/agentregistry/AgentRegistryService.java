package com.bfsi.platform.agentregistry;

import com.bfsi.platform.agents.common.AgentType;
import com.bfsi.platform.agents.common.registry.AgentRegistration;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class AgentRegistryService {

    private final Map<AgentType, AgentRegistration> registry = new ConcurrentHashMap<>();

    @Value("${agents.host:localhost}")
    private String agentHost;

    @PostConstruct
    void init() {
        int port = 8401;
        for (AgentType type : AgentType.values()) {
            register(type, port++);
        }
    }

    public void register(AgentType type, int port) {
        String baseUrl = "http://" + agentHost + ":" + port;
        registry.put(type, new AgentRegistration(
                type,
                type.getServiceName(),
                baseUrl,
                port,
                baseUrl + "/api/v1/agent/health",
                true
        ));
    }

    public Optional<AgentRegistration> find(AgentType type) {
        return Optional.ofNullable(registry.get(type));
    }

    public List<AgentRegistration> listAll() {
        return registry.values().stream()
                .sorted(Comparator.comparing(r -> r.type().name()))
                .toList();
    }

    public String resolveUrl(AgentType type) {
        return find(type)
                .map(AgentRegistration::baseUrl)
                .orElseThrow(() -> new IllegalArgumentException("Agent not registered: " + type));
    }
}
