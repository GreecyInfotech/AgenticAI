package com.bfsi.platform.agents.compliance;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.compliance.service.ComplianceAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class ComplianceAgentController extends AgentController {
    public ComplianceAgentController(ComplianceAgentService service) {
        super(service);
    }
}
