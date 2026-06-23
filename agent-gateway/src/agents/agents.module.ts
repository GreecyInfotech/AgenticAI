import { Module } from '@nestjs/common';
import { AgentsController } from './agents.controller';
import { AgentRouterService } from './agent-router.service';

@Module({
  controllers: [AgentsController],
  providers: [AgentRouterService],
  exports: [AgentRouterService],
})
export class AgentsModule {}
