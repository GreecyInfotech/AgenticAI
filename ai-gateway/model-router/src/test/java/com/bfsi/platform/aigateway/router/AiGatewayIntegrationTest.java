package com.bfsi.platform.aigateway.router;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("dev")
class AiGatewayIntegrationTest {

  @Autowired
  private MockMvc mockMvc;

  @Test
  void healthReturnsUp() throws Exception {
    mockMvc.perform(get("/api/v1/health"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("UP"));
  }

  @Test
  void chatUsesMockProviderWhenNoApiKey() throws Exception {
    String body = """
        {
          "agentType": "LOAN",
          "messages": [{"role": "user", "content": "Am I eligible for a home loan?"}]
        }
        """;

    mockMvc.perform(post("/api/v1/chat/completions")
            .contentType(MediaType.APPLICATION_JSON)
            .content(body))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.provider").value("MOCK"))
        .andExpect(jsonPath("$.content", containsString("MOCK")));
  }

  @Test
  void embeddingsUseMockProvider() throws Exception {
    String body = """
        {
          "input": "BFSI compliance check"
        }
        """;

    mockMvc.perform(post("/api/v1/embeddings")
            .contentType(MediaType.APPLICATION_JSON)
            .content(body))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.provider").value("MOCK"))
        .andExpect(jsonPath("$.embedding").isArray());
  }
}
