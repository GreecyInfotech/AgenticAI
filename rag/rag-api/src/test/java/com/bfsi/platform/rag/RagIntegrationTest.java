package com.bfsi.platform.rag;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
class RagIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void healthReturnsUp() throws Exception {
        mockMvc.perform(get("/api/v1/health"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("UP"));
    }

    @Test
    void collectionsListsAllAgents() throws Exception {
        mockMvc.perform(get("/api/v1/collections"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$", hasSize(14)));
    }

    @Test
    void retrieveLoanKnowledge() throws Exception {
        String body = """
            {"agentType":"LOAN","query":"home loan eligibility credit score","topK":2}
            """;

        mockMvc.perform(post("/api/v1/retrieve")
                .contentType(MediaType.APPLICATION_JSON)
                .content(body))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.agentType").value("LOAN"))
            .andExpect(jsonPath("$.chunks").isArray())
            .andExpect(jsonPath("$.chunks[0].content").exists());
    }
}
