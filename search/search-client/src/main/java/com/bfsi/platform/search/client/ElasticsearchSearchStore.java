package com.bfsi.platform.search.client;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.query_dsl.BoolQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.Query;
import co.elastic.clients.elasticsearch.core.IndexRequest;
import co.elastic.clients.elasticsearch.core.SearchRequest.Builder;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.json.jackson.JacksonJsonpMapper;
import co.elastic.clients.transport.rest_client.RestClientTransport;
import com.bfsi.platform.search.common.SearchDocument;
import com.bfsi.platform.search.common.SearchHit;
import com.bfsi.platform.search.common.SearchRequest;
import com.bfsi.platform.search.common.SearchResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class ElasticsearchSearchStore implements SearchStore {

    private static final Logger log = LoggerFactory.getLogger(ElasticsearchSearchStore.class);

    private final ElasticsearchClient client;
    private final String indexPrefix;
    private volatile boolean healthy;

    public ElasticsearchSearchStore(String host, int port, String indexPrefix) {
        this.indexPrefix = indexPrefix;
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        RestClient restClient = RestClient.builder(new HttpHost(host, port, "http")).build();
        RestClientTransport transport = new RestClientTransport(restClient, new JacksonJsonpMapper(mapper));
        this.client = new ElasticsearchClient(transport);
        this.healthy = ping();
    }

    @Override
    public void index(SearchDocument document) {
        try {
            String id = document.getId() != null ? document.getId() : UUID.randomUUID().toString();
            document.setId(id);
            client.index(IndexRequest.of(i -> i
                    .index(indexName(document.getIndexType()))
                    .id(id)
                    .document(document)));
        } catch (Exception e) {
            log.warn("Elasticsearch index failed: {}", e.getMessage());
            healthy = false;
            throw new SearchStoreException("Index failed", e);
        }
    }

    @Override
    public SearchResponse search(SearchRequest request) {
        long start = System.currentTimeMillis();
        try {
            BoolQuery.Builder bool = new BoolQuery.Builder()
                    .must(Query.of(q -> q.multiMatch(m -> m
                            .query(request.getQuery())
                            .fields("title^2", "content"))));
            if (request.getCustomerId() != null) {
                bool.filter(Query.of(q -> q.term(t -> t.field("customerId").value(request.getCustomerId()))));
            }
            if (request.getAgentType() != null) {
                bool.filter(Query.of(q -> q.term(t -> t.field("agentType").value(request.getAgentType()))));
            }

            var esResponse = client.search(new Builder()
                    .index(indexName(request.getIndexType()))
                    .query(Query.of(q -> q.bool(bool.build())))
                    .size(request.getSize())
                    .build(), Map.class);

            List<SearchHit> hits = new ArrayList<>();
            for (Hit<Map> hit : esResponse.hits().hits()) {
                Map source = hit.source();
                if (source == null) continue;
                SearchHit searchHit = new SearchHit();
                searchHit.setId(hit.id());
                searchHit.setTitle(String.valueOf(source.getOrDefault("title", "")));
                searchHit.setSnippet(String.valueOf(source.getOrDefault("content", "")));
                searchHit.setScore(hit.score() != null ? hit.score() : 0);
                searchHit.setIndexType(String.valueOf(source.getOrDefault("indexType", "")));
                searchHit.setAgentType((String) source.get("agentType"));
                searchHit.setCustomerId((String) source.get("customerId"));
                hits.add(searchHit);
            }

            SearchResponse response = new SearchResponse();
            response.setQuery(request.getQuery());
            response.setTotalHits(esResponse.hits().total() != null ? esResponse.hits().total().value() : hits.size());
            response.setTookMs(System.currentTimeMillis() - start);
            response.setHits(hits);
            healthy = true;
            return response;
        } catch (Exception e) {
            log.warn("Elasticsearch search failed: {}", e.getMessage());
            healthy = false;
            throw new SearchStoreException("Search failed", e);
        }
    }

    @Override
    public boolean isHealthy() {
        return healthy;
    }

    @Override
    public String backend() {
        return "elasticsearch";
    }

    private boolean ping() {
        try {
            return client.ping().value();
        } catch (Exception e) {
            return false;
        }
    }

    private String indexName(String indexType) {
        return indexPrefix + "-" + (indexType != null ? indexType : "documents");
    }
}
