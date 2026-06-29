package com.bfsi.platform.agents.loan;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.loan.service.LoanAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class LoanAgentController extends AgentController {
    public LoanAgentController(LoanAgentService service) {
        super(service);
    }
}
