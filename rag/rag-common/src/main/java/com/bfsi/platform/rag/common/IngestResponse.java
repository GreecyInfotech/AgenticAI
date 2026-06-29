package com.bfsi.platform.rag.common;

public class IngestResponse {

    private String requestId;
    private int documentsIngested;
    private int chunksCreated;
    private long latencyMs;

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public int getDocumentsIngested() { return documentsIngested; }
    public void setDocumentsIngested(int documentsIngested) { this.documentsIngested = documentsIngested; }
    public int getChunksCreated() { return chunksCreated; }
    public void setChunksCreated(int chunksCreated) { this.chunksCreated = chunksCreated; }
    public long getLatencyMs() { return latencyMs; }
    public void setLatencyMs(long latencyMs) { this.latencyMs = latencyMs; }
}
