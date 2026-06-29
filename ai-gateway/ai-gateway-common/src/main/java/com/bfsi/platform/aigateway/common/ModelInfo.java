package com.bfsi.platform.aigateway.common;

public record ModelInfo(String id, String displayName, ModelProvider provider, TaskType taskType, int maxTokens) {
}
