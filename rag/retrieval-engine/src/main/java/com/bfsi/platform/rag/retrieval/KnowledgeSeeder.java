package com.bfsi.platform.rag.retrieval;

import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class KnowledgeSeeder {

    private static final Logger log = LoggerFactory.getLogger(KnowledgeSeeder.class);

    private final DocumentIngestionService ingestionService;

    public KnowledgeSeeder(DocumentIngestionService ingestionService) {
        this.ingestionService = ingestionService;
    }

    @PostConstruct
    void seed() {
        log.info("Seeding BFSI knowledge corpus for all agents...");
        ingestionService.seedIfEmpty();
        log.info("Knowledge corpus seeding complete");
    }
}
