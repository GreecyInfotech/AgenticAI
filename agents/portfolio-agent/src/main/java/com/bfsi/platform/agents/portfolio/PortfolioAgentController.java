package com.bfsi.platform.agents.portfolio;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.portfolio.service.PortfolioAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class PortfolioAgentController extends AgentController {
    public PortfolioAgentController(PortfolioAgentService service) {
        super(service);
    }
}
