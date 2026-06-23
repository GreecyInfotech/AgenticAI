import { Controller, Post, Body, UseGuards, Req } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags, ApiOperation } from '@nestjs/swagger';
import { IsString } from 'class-validator';
import { OrchestrationService } from './orchestration.service';

class WorkflowDto {
  @IsString()
  intent!: string;
}

@ApiTags('orchestration')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('orchestrate')
export class OrchestrationController {
  constructor(private readonly orchestration: OrchestrationService) {}

  @Post()
  @ApiOperation({ summary: 'Multi-agent orchestrated workflow' })
  async orchestrate(@Body() dto: WorkflowDto, @Req() req: { headers: { authorization?: string } }) {
    const token = req.headers.authorization?.replace('Bearer ', '') || '';
    const plan = this.orchestration.planMultiAgentWorkflow(dto.intent);
    return this.orchestration.executeWorkflow(plan, token);
  }
}
