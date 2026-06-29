package com.bfsi.platform.agents.underwriting;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.underwriting.service.UnderwritingAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class UnderwritingAgentController extends AgentController {
    public UnderwritingAgentController(UnderwritingAgentService service) {
        super(service);
    }
}
