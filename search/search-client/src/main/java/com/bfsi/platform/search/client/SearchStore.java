package com.bfsi.platform.search.client;

import com.bfsi.platform.search.common.SearchDocument;
import com.bfsi.platform.search.common.SearchRequest;
import com.bfsi.platform.search.common.SearchResponse;

public interface SearchStore {

    void index(SearchDocument document);

    SearchResponse search(SearchRequest request);

    boolean isHealthy();

    String backend();
}
