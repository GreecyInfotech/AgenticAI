package com.bfsi.platform.search.common;

import java.util.ArrayList;
import java.util.List;

public class SearchResponse {

    private String query;
    private long totalHits;
    private long tookMs;
    private List<SearchHit> hits = new ArrayList<>();

    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    public long getTotalHits() { return totalHits; }
    public void setTotalHits(long totalHits) { this.totalHits = totalHits; }
    public long getTookMs() { return tookMs; }
    public void setTookMs(long tookMs) { this.tookMs = tookMs; }
    public List<SearchHit> getHits() { return hits; }
    public void setHits(List<SearchHit> hits) { this.hits = hits != null ? hits : new ArrayList<>(); }
}
