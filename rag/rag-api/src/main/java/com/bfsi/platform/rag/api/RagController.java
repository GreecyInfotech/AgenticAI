package com.bfsi.platform.rag.api;

import com.bfsi.platform.rag.common.*;
import com.bfsi.platform.rag.retrieval.RetrievalService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class RagController {

    private final RetrievalService retrievalService;

    public RagController(RetrievalService retrievalService) {
        this.retrievalService = retrievalService;
    }

    @PostMapping("/retrieve")
    public ResponseEntity<RetrievalResponse> retrieve(@Valid @RequestBody RetrievalRequest request) {
        return ResponseEntity.ok(retrievalService.retrieve(request));
    }

    @PostMapping("/ingest")
    public ResponseEntity<IngestResponse> ingest(@Valid @RequestBody IngestRequest request) {
        return ResponseEntity.ok(retrievalService.ingest(request));
    }

    @GetMapping("/collections")
    public ResponseEntity<List<CollectionInfo>> collections() {
        return ResponseEntity.ok(retrievalService.listCollections());
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "UP", "service", "rag-api"));
    }
}
