package com.bfsi.platform.agents.recommendation;

import com.bfsi.platform.agents.common.web.AgentController;
import com.bfsi.platform.agents.recommendation.service.RecommendationAgentService;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/agent")
public class RecommendationAgentController extends AgentController {
    public RecommendationAgentController(RecommendationAgentService service) {
        super(service);
    }
}
