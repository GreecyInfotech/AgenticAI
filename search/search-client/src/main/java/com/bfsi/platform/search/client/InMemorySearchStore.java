package com.bfsi.platform.search.client;

import com.bfsi.platform.search.common.SearchDocument;
import com.bfsi.platform.search.common.SearchHit;
import com.bfsi.platform.search.common.SearchRequest;
import com.bfsi.platform.search.common.SearchResponse;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

public class InMemorySearchStore implements SearchStore {

    private final Map<String, SearchDocument> documents = new ConcurrentHashMap<>();

    @Override
    public void index(SearchDocument document) {
        String id = document.getId() != null ? document.getId() : UUID.randomUUID().toString();
        document.setId(id);
        documents.put(id, document);
    }

    @Override
    public SearchResponse search(SearchRequest request) {
        long start = System.currentTimeMillis();
        String query = request.getQuery().toLowerCase(Locale.ROOT);
        List<SearchHit> hits = documents.values().stream()
                .filter(doc -> matchesIndexType(doc, request.getIndexType()))
                .filter(doc -> request.getCustomerId() == null || request.getCustomerId().equals(doc.getCustomerId()))
                .filter(doc -> request.getAgentType() == null || request.getAgentType().equals(doc.getAgentType()))
                .map(doc -> score(doc, query))
                .filter(hit -> hit.getScore() > 0)
                .sorted(Comparator.comparingDouble(SearchHit::getScore).reversed())
                .limit(request.getSize())
                .collect(Collectors.toList());

        SearchResponse response = new SearchResponse();
        response.setQuery(request.getQuery());
        response.setTotalHits(hits.size());
        response.setTookMs(System.currentTimeMillis() - start);
        response.setHits(hits);
        return response;
    }

    @Override
    public boolean isHealthy() {
        return true;
    }

    @Override
    public String backend() {
        return "memory";
    }

    private static boolean matchesIndexType(SearchDocument doc, String indexType) {
        return indexType == null || indexType.equals(doc.getIndexType());
    }

    private static SearchHit score(SearchDocument doc, String query) {
        String haystack = (doc.getTitle() + " " + doc.getContent()).toLowerCase(Locale.ROOT);
        double score = 0;
        for (String term : query.split("\\s+")) {
            if (!term.isBlank() && haystack.contains(term)) {
                score += 1.0;
            }
        }
        if (doc.getTitle().toLowerCase(Locale.ROOT).contains(query)) {
            score += 2.0;
        }
        SearchHit hit = new SearchHit();
        hit.setId(doc.getId());
        hit.setTitle(doc.getTitle());
        hit.setSnippet(snippet(doc.getContent(), 160));
        hit.setScore(score);
        hit.setIndexType(doc.getIndexType());
        hit.setAgentType(doc.getAgentType());
        hit.setCustomerId(doc.getCustomerId());
        return hit;
    }

    private static String snippet(String content, int maxLen) {
        if (content == null) return "";
        return content.length() <= maxLen ? content : content.substring(0, maxLen) + "...";
    }
}
