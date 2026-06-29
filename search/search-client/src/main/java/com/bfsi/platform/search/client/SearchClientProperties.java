package com.bfsi.platform.search.client;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "search")
public class SearchClientProperties {

    private String backend = "memory";
    private String host = "localhost";
    private int port = 9200;
    private String indexPrefix = "bfsi";

    public String getBackend() { return backend; }
    public void setBackend(String backend) { this.backend = backend; }
    public String getHost() { return host; }
    public void setHost(String host) { this.host = host; }
    public int getPort() { return port; }
    public void setPort(int port) { this.port = port; }
    public String getIndexPrefix() { return indexPrefix; }
    public void setIndexPrefix(String indexPrefix) { this.indexPrefix = indexPrefix; }
}
