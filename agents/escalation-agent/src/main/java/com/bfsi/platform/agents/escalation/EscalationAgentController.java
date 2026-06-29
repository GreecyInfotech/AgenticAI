package com.bfsi.platform.agents.escalation;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.escalation.service.EscalationAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class EscalationAgentController extends AgentController {
    public EscalationAgentController(EscalationAgentService service) {
        super(service);
    }
}
