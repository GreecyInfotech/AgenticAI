package com.bfsi.platform.rag.common;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;

import java.util.ArrayList;
import java.util.List;

public class IngestRequest {

    private String requestId;

    @NotEmpty
    @Valid
    private List<DocumentInput> documents = new ArrayList<>();

    public String getRequestId() { return requestId; }
    public void setRequestId(String requestId) { this.requestId = requestId; }
    public List<DocumentInput> getDocuments() { return documents; }
    public void setDocuments(List<DocumentInput> documents) {
        this.documents = documents != null ? documents : new ArrayList<>();
    }
}
