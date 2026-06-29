package com.bfsi.platform.aigateway.common;

public record PromptTemplate(
    String id,
    String name,
    String agentType,
    String systemPrompt,
    String userPromptTemplate,
    String version
) {
}
