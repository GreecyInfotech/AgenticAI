package com.bfsi.platform.agents.common;

public interface BfsiAgent {

    AgentType getType();

    AgentCapabilities getCapabilities();

    AgentResponse process(AgentRequest request);
}
