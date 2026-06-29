package com.bfsi.platform.agents.aml;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.aml.service.AmlAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class AmlAgentController extends AgentController {
    public AmlAgentController(AmlAgentService service) {
        super(service);
    }
}
