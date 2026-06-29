package com.bfsi.platform.agents.common.domain;

public record DocumentCheck(
        String documentType,
        String documentId,
        boolean valid,
        String validationMessage
) {
}
