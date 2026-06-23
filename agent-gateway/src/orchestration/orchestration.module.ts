import { Module } from '@nestjs/common';
import { AgentsModule } from '../agents/agents.module';
import { OrchestrationController } from './orchestration.controller';
import { OrchestrationService } from './orchestration.service';

@Module({
  imports: [AgentsModule],
  controllers: [OrchestrationController],
  providers: [OrchestrationService],
})
export class OrchestrationModule {}
