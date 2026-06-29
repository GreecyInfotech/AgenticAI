package com.bfsi.platform.orchestrator;

import com.bfsi.platform.agents.common.AgentRequest;
import com.bfsi.platform.agents.common.AgentType;
import com.bfsi.platform.rag.common.RagContextKeys;
import com.bfsi.platform.rag.common.RetrievalRequest;
import com.bfsi.platform.rag.common.RetrievalResponse;
import com.bfsi.platform.rag.common.RetrievedChunk;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Component
public class RagClient {

    private static final Logger log = LoggerFactory.getLogger(RagClient.class);

    private final RestTemplate restTemplate;
    private final String ragUrl;
    private final boolean enabled;

    public RagClient(RestTemplate restTemplate,
                     @Value("${rag.url:http://localhost:8350}") String ragUrl,
                     @Value("${rag.enabled:true}") boolean enabled) {
        this.restTemplate = restTemplate;
        this.ragUrl = ragUrl;
        this.enabled = enabled;
    }

    public void enrichRequest(AgentRequest request, AgentType agentType) {
        if (!enabled || request.getUserMessage() == null || request.getUserMessage().isBlank()) {
            return;
        }
        try {
            RetrievalRequest ragRequest = new RetrievalRequest();
            ragRequest.setRequestId(request.getRequestId());
            ragRequest.setAgentType(agentType);
            ragRequest.setQuery(request.getUserMessage());
            ragRequest.setTopK(3);

            RetrievalResponse response = restTemplate.postForObject(
                ragUrl + "/api/v1/retrieve",
                ragRequest,
                RetrievalResponse.class
            );

            if (response != null && response.getChunks() != null && !response.getChunks().isEmpty()) {
                request.getContext().put(RagContextKeys.CHUNKS, response.getChunks());
                request.getContext().put(RagContextKeys.COLLECTION, response.getCollection());
                request.getContext().put("ragInsight", formatInsight(response.getChunks()));
                log.debug("RAG enriched {} with {} chunks", agentType, response.getChunks().size());
            }
        } catch (Exception ex) {
            log.warn("RAG retrieval failed for {}: {}", agentType, ex.getMessage());
        }
    }

    private static String formatInsight(List<RetrievedChunk> chunks) {
        RetrievedChunk top = chunks.getFirst();
        String title = top.getTitle() != null ? top.getTitle() : "Knowledge";
        String content = top.getContent();
        if (content.length() > 250) {
            content = content.substring(0, 247) + "...";
        }
        return title + ": " + content;
    }
}
