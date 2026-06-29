package com.bfsi.platform.agents.customer;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.customer.service.CustomerAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class CustomerAgentController extends AgentController {
    public CustomerAgentController(CustomerAgentService service) {
        super(service);
    }
}
