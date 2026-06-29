package com.bfsi.platform.agents.claim;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.claim.service.ClaimAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class ClaimAgentController extends AgentController {
    public ClaimAgentController(ClaimAgentService service) {
        super(service);
    }
}
