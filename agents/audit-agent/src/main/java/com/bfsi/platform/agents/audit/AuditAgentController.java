package com.bfsi.platform.agents.audit;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.audit.service.AuditAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class AuditAgentController extends AgentController {
    public AuditAgentController(AuditAgentService service) {
        super(service);
    }
}
