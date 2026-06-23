import { Injectable } from '@nestjs/common';
import { AgentRouterService } from '../agents/agent-router.service';
import { AGENT_REGISTRY } from 'smart-port-types';

export interface OrchestrationPlan {
  steps: Array<{ agent: string; query: string }>;
}

@Injectable()
export class OrchestrationService {
  constructor(private readonly agentRouter: AgentRouterService) {}

  planMultiAgentWorkflow(intent: string): OrchestrationPlan {
    const intentLower = intent.toLowerCase();
    const steps: OrchestrationPlan['steps'] = [];

    if (intentLower.includes('vessel') || intentLower.includes('berth')) {
      steps.push({ agent: 'vessel', query: intent });
    }
    if (intentLower.includes('container') || intentLower.includes('yard')) {
      steps.push({ agent: 'container', query: intent });
    }
    if (intentLower.includes('customs') || intentLower.includes('clearance')) {
      steps.push({ agent: 'customs', query: intent });
    }
    if (intentLower.includes('weather')) {
      steps.push({ agent: 'weather', query: intent });
    }
    if (intentLower.includes('billing') || intentLower.includes('invoice')) {
      steps.push({ agent: 'billing', query: intent });
    }
    if (steps.length === 0) {
      steps.push({ agent: 'planning', query: intent });
    }
    if (intentLower.includes('executive') || intentLower.includes('kpi')) {
      steps.push({ agent: 'executive', query: `Summarize: ${intent}` });
    }

    return { steps };
  }

  async executeWorkflow(plan: OrchestrationPlan, token: string) {
    const results = [];
    for (const step of plan.steps) {
      if (!(step.agent in AGENT_REGISTRY)) continue;
      const result = await this.agentRouter.invoke(
        step.agent as keyof typeof AGENT_REGISTRY,
        { query: step.query },
        token,
      );
      results.push({ agent: step.agent, result });
    }
    return { workflow: plan, results, completed_at: new Date().toISOString() };
  }
}
