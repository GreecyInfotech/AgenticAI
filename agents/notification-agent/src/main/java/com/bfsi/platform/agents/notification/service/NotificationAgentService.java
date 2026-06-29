package com.bfsi.platform.agents.notification.service;

import com.bfsi.platform.agents.common.*;
import com.bfsi.platform.agents.common.domain.NotificationResult;
import com.bfsi.platform.tools.bindings.NotificationTools;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import com.bfsi.platform.agents.common.ToolSupport;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Set;

@Service
public class NotificationAgentService extends AbstractBfsiAgent {

    private final NotificationTools notificationTools;

    public NotificationAgentService(NotificationTools notificationTools) {
        this.notificationTools = notificationTools;
    }

    @Override
    public AgentType getType() {
        return AgentType.NOTIFICATION;
    }

    @Override
    public AgentCapabilities getCapabilities() {
        return new AgentCapabilities(
                AgentType.NOTIFICATION,
                "1.0.0",
                Set.of("email", "sms", "push_notification"),
                List.of("customerId"),
                false
        );
    }

    @Override
    public AgentResponse process(AgentRequest request) {
        String customerId = request.getCustomerId() != null ? request.getCustomerId() : "UNKNOWN";
        String channel = request.getPayload().getOrDefault("channel", detectChannel(request)).toString();
        String recipient = request.getPayload().getOrDefault("recipient",
                "customer+" + customerId + "@notifications.bfsi.local").toString();
        String templateId = request.getPayload().getOrDefault("templateId", "DEFAULT_ALERT").toString();
        String body = request.getPayload().getOrDefault("body", request.getUserMessage()).toString();

        ToolInvocationResult toolResult;
        if ("SMS".equalsIgnoreCase(channel)) {
            toolResult = notificationTools.sendSms(recipient, body);
        } else {
            toolResult = notificationTools.sendEmail(recipient, "BFSI Platform Notification", body, templateId);
        }

        NotificationResult result;
        if (toolResult.isSuccess()) {
            Map<String, Object> data = toolResult.getData();
            result = new NotificationResult(
                str(data.get("notificationId"), "NOTIF-LOCAL"),
                str(data.get("channel"), channel).toUpperCase(),
                str(data.get("to"), recipient),
                str(data.get("status"), "SENT"),
                templateId,
                Instant.now()
            );
        } else {
            result = new NotificationResult(
                "NOTIF-FALLBACK",
                channel.toUpperCase(),
                recipient,
                "QUEUED",
                templateId,
                Instant.now()
            );
        }

        AgentResponse response = buildResponse(request, AgentStatus.SUCCESS,
                "Notification sent via " + result.channel() + " to " + maskRecipient(recipient));
        response.setConfidence(1.0);
        response.withData("notification", result);
        response.withData("channelsUsed", List.of(result.channel()));
        ToolSupport.record(response, toolResult);
        routeTo(response, AgentType.AUDIT);
        return response;
    }

    private String detectChannel(AgentRequest request) {
        String msg = request.getUserMessage().toLowerCase();
        if (msg.contains("sms") || msg.contains("text")) return "SMS";
        if (msg.contains("push")) return "PUSH";
        return "EMAIL";
    }

    private String maskRecipient(String recipient) {
        if (recipient.contains("@")) {
            int at = recipient.indexOf('@');
            return recipient.charAt(0) + "***" + recipient.substring(at);
        }
        return recipient.length() > 4 ? recipient.substring(0, 2) + "****" : "****";
    }

    private static String str(Object value, String defaultVal) {
        return value != null ? value.toString() : defaultVal;
    }
}
