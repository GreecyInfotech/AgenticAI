package com.bfsi.platform.agents.kyc;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.kyc.service.KycAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class KycAgentController extends AgentController {
    public KycAgentController(KycAgentService service) {
        super(service);
    }
}
