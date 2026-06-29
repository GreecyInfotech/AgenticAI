package com.bfsi.platform.rag.embedding;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;

@Component
public class EmbeddingClient {

    private static final Logger log = LoggerFactory.getLogger(EmbeddingClient.class);

    private final EmbeddingClientProperties properties;
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public EmbeddingClient(EmbeddingClientProperties properties,
                           RestTemplate embeddingRestTemplate,
                           ObjectMapper ragObjectMapper) {
        this.properties = properties;
        this.restTemplate = embeddingRestTemplate;
        this.objectMapper = ragObjectMapper;
    }

    public List<Double> embed(String text) {
        try {
            return embedViaAiGateway(text);
        } catch (Exception ex) {
            log.warn("AI Gateway embedding failed, using local fallback: {}", ex.getMessage());
            if (properties.isFallbackToLocal()) {
                return localEmbedding(text, properties.getDimensions());
            }
            throw new EmbeddingException("Embedding failed: " + ex.getMessage(), ex);
        }
    }

    private List<Double> embedViaAiGateway(String text) {
        ObjectNode body = objectMapper.createObjectNode();
        body.put("input", text);
        body.put("model", properties.getModel());

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        ResponseEntity<String> response = restTemplate.exchange(
            properties.getAiGatewayUrl() + "/api/v1/embeddings",
            HttpMethod.POST,
            new HttpEntity<>(body.toString(), headers),
            String.class
        );

        try {
            JsonNode root = objectMapper.readTree(response.getBody());
            List<Double> vector = new ArrayList<>();
            root.path("embedding").forEach(n -> vector.add(n.asDouble()));
            if (vector.isEmpty()) {
                throw new EmbeddingException("Empty embedding vector from AI Gateway");
            }
            return vector;
        } catch (EmbeddingException e) {
            throw e;
        } catch (Exception e) {
            throw new EmbeddingException("Failed to parse embedding response", e);
        }
    }

    public static List<Double> localEmbedding(String input, int dimensions) {
        try {
            byte[] hash = MessageDigest.getInstance("SHA-256")
                .digest(input.getBytes(StandardCharsets.UTF_8));
            List<Double> vector = new ArrayList<>(dimensions);
            for (int i = 0; i < dimensions; i++) {
                vector.add((hash[i % hash.length] & 0xFF) / 255.0 - 0.5);
            }
            double norm = Math.sqrt(vector.stream().mapToDouble(v -> v * v).sum());
            if (norm == 0) return vector;
            return vector.stream().map(v -> v / norm).toList();
        } catch (Exception e) {
            return List.of();
        }
    }
}
