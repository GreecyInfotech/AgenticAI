package com.bfsi.platform.rag.common;

import com.bfsi.platform.agents.common.AgentRequest;
import com.bfsi.platform.agents.common.AgentResponse;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Collections;
import java.util.List;
import java.util.Map;

public final class RagContextHelper {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private RagContextHelper() {}

    @SuppressWarnings("unchecked")
    public static List<RetrievedChunk> getChunks(AgentRequest request) {
        if (request == null || request.getContext() == null) {
            return Collections.emptyList();
        }
        Object raw = request.getContext().get(RagContextKeys.CHUNKS);
        if (raw == null) {
            return Collections.emptyList();
        }
        if (raw instanceof List<?> list) {
            return MAPPER.convertValue(list, new TypeReference<List<RetrievedChunk>>() {});
        }
        return Collections.emptyList();
    }

    public static String formatTopInsight(AgentRequest request) {
        List<RetrievedChunk> chunks = getChunks(request);
        if (chunks.isEmpty()) {
            return "";
        }
        RetrievedChunk top = chunks.getFirst();
        String title = top.getTitle() != null ? top.getTitle() : "Knowledge base";
        String snippet = top.getContent();
        if (snippet.length() > 280) {
            snippet = snippet.substring(0, 277) + "...";
        }
        return title + ": " + snippet;
    }

    public static void attachToResponse(AgentRequest request, AgentResponse response) {
        List<RetrievedChunk> chunks = getChunks(request);
        if (chunks.isEmpty()) {
            return;
        }
        response.withData("ragChunks", chunks);
        response.withData("ragInsight", formatTopInsight(request));
        Object collection = request.getContext().get(RagContextKeys.COLLECTION);
        if (collection != null) {
            response.withData("ragCollection", collection);
        }
    }
}
