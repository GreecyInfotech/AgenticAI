package com.bfsi.platform.aigateway.common;

public class GatewayException extends RuntimeException {

  private final String errorCode;

  public GatewayException(String errorCode, String message) {
    super(message);
    this.errorCode = errorCode;
  }

  public String getErrorCode() {
    return errorCode;
  }
}
