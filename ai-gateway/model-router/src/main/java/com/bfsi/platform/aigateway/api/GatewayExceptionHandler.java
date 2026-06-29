package com.bfsi.platform.aigateway.api;

import com.bfsi.platform.aigateway.common.GatewayException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Map;

@RestControllerAdvice
public class GatewayExceptionHandler {

  @ExceptionHandler(GatewayException.class)
  public ResponseEntity<Map<String, Object>> handleGateway(GatewayException ex) {
    HttpStatus status = switch (ex.getErrorCode()) {
      case "TOKEN_LIMIT_EXCEEDED", "SESSION_TOKEN_LIMIT" -> HttpStatus.TOO_MANY_REQUESTS;
      case "GUARDRAIL_VIOLATION", "PII_DETECTED" -> HttpStatus.UNPROCESSABLE_ENTITY;
      case "PROMPT_NOT_FOUND", "NO_PROVIDER", "PROVIDER_NOT_CONFIGURED" -> HttpStatus.BAD_REQUEST;
      case "PROVIDER_ERROR" -> HttpStatus.BAD_GATEWAY;
      default -> HttpStatus.INTERNAL_SERVER_ERROR;
    };
    return ResponseEntity.status(status).body(Map.of(
        "error", ex.getErrorCode(),
        "message", ex.getMessage()
    ));
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
    String message = ex.getBindingResult().getFieldErrors().stream()
        .map(e -> e.getField() + ": " + e.getDefaultMessage())
        .reduce((a, b) -> a + "; " + b)
        .orElse("Validation failed");
    return ResponseEntity.badRequest().body(Map.of("error", "VALIDATION_ERROR", "message", message));
  }

  @ExceptionHandler(Exception.class)
  public ResponseEntity<Map<String, Object>> handleUnexpected(Exception ex) {
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
        "error", "INTERNAL_ERROR",
        "message", ex.getMessage() != null ? ex.getMessage() : "Unexpected error"
    ));
  }
}
