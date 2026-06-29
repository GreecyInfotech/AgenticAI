package com.bfsi.platform.aigateway.common;

import com.bfsi.platform.aigateway.common.ChatCompletionRequest;
import com.bfsi.platform.aigateway.common.ChatCompletionResponse;
import com.bfsi.platform.aigateway.common.EmbeddingRequest;
import com.bfsi.platform.aigateway.common.EmbeddingResponse;
import com.bfsi.platform.aigateway.common.ModelProvider;

public interface LlmProvider {

  ModelProvider provider();

  boolean supports(String model);

  ChatCompletionResponse chat(ChatCompletionRequest request, String resolvedModel);

  EmbeddingResponse embed(EmbeddingRequest request, String resolvedModel);
}
