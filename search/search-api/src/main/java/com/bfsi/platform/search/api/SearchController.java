package com.bfsi.platform.search.api;

import com.bfsi.platform.search.client.SearchStore;
import com.bfsi.platform.search.common.*;
import jakarta.annotation.PostConstruct;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class SearchController {

    private final SearchStore searchStore;

    public SearchController(SearchStore searchStore) {
        this.searchStore = searchStore;
    }

    @PostConstruct
    void seedDemoDocuments() {
        indexQuiet(demo("BFSI Loan Policy", "Home loan eligibility requires minimum credit score 650 and debt-to-income below 45%.", SearchIndexTypes.DOCUMENTS, "LOAN"));
        indexQuiet(demo("KYC Master Direction", "RBI KYC norms require periodic re-KYC for high-risk customers every two years.", SearchIndexTypes.DOCUMENTS, "KYC"));
        indexQuiet(demo("AML Screening Guide", "PEP and sanctions screening must be performed before account opening.", SearchIndexTypes.DOCUMENTS, "AML"));
        indexQuiet(demo("Customer CUST-12345", "Premium banking customer with home loan and investment portfolio.", SearchIndexTypes.CUSTOMERS, "CUSTOMER"));
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        return ResponseEntity.ok(Map.of(
                "status", searchStore.isHealthy() ? "UP" : "DEGRADED",
                "service", "search-api",
                "backend", searchStore.backend()
        ));
    }

    @PostMapping("/search")
    public ResponseEntity<SearchResponse> search(@Valid @RequestBody SearchRequest request) {
        return ResponseEntity.ok(searchStore.search(request));
    }

    @PostMapping("/index")
    public ResponseEntity<Map<String, String>> index(@Valid @RequestBody SearchDocument document) {
        searchStore.index(document);
        return ResponseEntity.ok(Map.of("id", document.getId(), "status", "INDEXED"));
    }

    @GetMapping("/indices")
    public ResponseEntity<List<Map<String, String>>> indices() {
        return ResponseEntity.ok(List.of(
                index(SearchIndexTypes.DOCUMENTS, "Platform documents and policies"),
                index(SearchIndexTypes.AUDIT, "Audit and compliance records"),
                index(SearchIndexTypes.CUSTOMERS, "Customer profiles"),
                index(SearchIndexTypes.AGENT_DECISIONS, "AI agent decision history")
        ));
    }

    private void indexQuiet(SearchDocument doc) {
        try {
            searchStore.index(doc);
        } catch (Exception ignored) {
            // seed is best-effort when elasticsearch is unavailable
        }
    }

    private static SearchDocument demo(String title, String content, String indexType, String agentType) {
        SearchDocument doc = new SearchDocument();
        doc.setTitle(title);
        doc.setContent(content);
        doc.setIndexType(indexType);
        doc.setAgentType(agentType);
        doc.setSource("seed");
        return doc;
    }

    private static Map<String, String> index(String name, String description) {
        return Map.of("name", name, "description", description);
    }
}
