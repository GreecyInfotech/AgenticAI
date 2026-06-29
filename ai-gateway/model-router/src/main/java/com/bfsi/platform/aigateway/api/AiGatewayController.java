package com.bfsi.platform.aigateway.api;

import com.bfsi.platform.aigateway.common.*;
import com.bfsi.platform.aigateway.prompt.PromptRouterService;
import com.bfsi.platform.aigateway.router.AiGatewayService;
import com.bfsi.platform.aigateway.router.ModelRouterService;
import com.bfsi.platform.aigateway.token.TokenBudgetService;
import com.bfsi.platform.aigateway.token.TokenUsageTracker;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class AiGatewayController {

  private final AiGatewayService gatewayService;
  private final ModelRouterService modelRouter;
  private final PromptRouterService promptRouter;
  private final TokenUsageTracker usageTracker;
  private final TokenBudgetService tokenBudget;

  public AiGatewayController(AiGatewayService gatewayService,
                             ModelRouterService modelRouter,
                             PromptRouterService promptRouter,
                             TokenUsageTracker usageTracker,
                             TokenBudgetService tokenBudget) {
    this.gatewayService = gatewayService;
    this.modelRouter = modelRouter;
    this.promptRouter = promptRouter;
    this.usageTracker = usageTracker;
    this.tokenBudget = tokenBudget;
  }

  @PostMapping("/chat/completions")
  public ResponseEntity<ChatCompletionResponse> chat(@Valid @RequestBody ChatCompletionRequest request) {
    return ResponseEntity.ok(gatewayService.chat(request));
  }

  @PostMapping("/embeddings")
  public ResponseEntity<EmbeddingResponse> embed(@Valid @RequestBody EmbeddingRequest request) {
    return ResponseEntity.ok(gatewayService.embed(request));
  }

  @GetMapping("/models")
  public ResponseEntity<List<ModelInfo>> models() {
    return ResponseEntity.ok(modelRouter.listModels());
  }

  @GetMapping("/prompts")
  public ResponseEntity<List<PromptTemplate>> prompts() {
    return ResponseEntity.ok(promptRouter.listTemplates());
  }

  @GetMapping("/prompts/{templateId}")
  public ResponseEntity<PromptTemplate> prompt(@PathVariable String templateId) {
    return ResponseEntity.ok(promptRouter.getTemplate(templateId));
  }

  @GetMapping("/usage")
  public ResponseEntity<Map<String, Object>> usage() {
    return ResponseEntity.ok(usageTracker.snapshot());
  }

  @GetMapping("/usage/session/{sessionId}")
  public ResponseEntity<Map<String, Object>> sessionUsage(@PathVariable String sessionId) {
    return ResponseEntity.ok(Map.of(
        "sessionId", sessionId,
        "tokensUsed", tokenBudget.getSessionUsage(sessionId)
    ));
  }

  @GetMapping("/health")
  public ResponseEntity<Map<String, String>> health() {
    return ResponseEntity.ok(Map.of("status", "UP", "service", "ai-gateway"));
  }
}
