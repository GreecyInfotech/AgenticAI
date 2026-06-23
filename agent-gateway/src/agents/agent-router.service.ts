import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import axios from 'axios';
import { AGENT_REGISTRY, AgentRequest, AgentResponse } from 'smart-port-types';

@Injectable()
export class AgentRouterService {
  private getAgentUrl(agentKey: keyof typeof AGENT_REGISTRY): string {
    const agent = AGENT_REGISTRY[agentKey];
    const host = process.env[`${agent.name.toUpperCase().replace(/-/g, '_')}_URL`]
      || `http://localhost:${agent.port}`;
    return host;
  }

  async invoke(agentKey: keyof typeof AGENT_REGISTRY, request: AgentRequest, token: string): Promise<AgentResponse> {
    const url = `${this.getAgentUrl(agentKey)}/invoke`;
    try {
      const { data } = await axios.post<AgentResponse>(url, request, {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 120000,
      });
      return data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new HttpException(
          error.response?.data || 'Agent invocation failed',
          error.response?.status || HttpStatus.BAD_GATEWAY,
        );
      }
      throw error;
    }
  }

  listAgents() {
    return Object.entries(AGENT_REGISTRY).map(([key, agent]) => ({
      key,
      name: agent.name,
      domain: agent.domain,
      port: agent.port,
    }));
  }
}
