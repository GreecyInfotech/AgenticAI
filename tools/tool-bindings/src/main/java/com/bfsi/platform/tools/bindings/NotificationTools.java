package com.bfsi.platform.tools.bindings;

import com.bfsi.platform.tools.common.ToolExecutor;
import com.bfsi.platform.tools.common.ToolInvocationResult;
import org.springframework.stereotype.Component;

import java.util.Map;

@Component
public class NotificationTools extends AbstractToolBinding {

    private static final String SERVER = "email";

    public NotificationTools(ToolExecutor executor) {
        super(executor);
    }

    public ToolInvocationResult sendEmail(String to, String subject, String body, String templateId) {
        return call(SERVER, "send_email", Map.of(
            "to", to,
            "subject", subject,
            "body", body,
            "templateId", templateId != null ? templateId : "DEFAULT"
        ));
    }

    public ToolInvocationResult sendSms(String to, String message) {
        return call(SERVER, "send_sms", Map.of("to", to, "message", message));
    }

    public ToolInvocationResult getDeliveryStatus(String notificationId) {
        return call(SERVER, "get_delivery_status", args("notificationId", notificationId));
    }
}
