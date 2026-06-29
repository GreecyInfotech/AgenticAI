package com.bfsi.platform.agents.intent;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.intent.service.IntentAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class IntentAgentController extends AgentController {
    public IntentAgentController(IntentAgentService service) {
        super(service);
    }
}
