package com.bfsi.platform.agents.common.domain;

import java.util.List;

public record ComplianceCheck(
        String checkId,
        String regulation,
        boolean compliant,
        List<String> violations,
        List<String> recommendations,
        String severity
) {
}
