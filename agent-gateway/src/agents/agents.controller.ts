import { Controller, Post, Get, Param, Body, UseGuards, Req } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags, ApiOperation } from '@nestjs/swagger';
import { IsString, IsOptional, IsObject } from 'class-validator';
import { AgentRouterService } from './agent-router.service';
import { AGENT_REGISTRY } from 'smart-port-types';

class InvokeDto {
  @IsString()
  query!: string;

  @IsOptional()
  @IsObject()
  context?: Record<string, unknown>;

  @IsOptional()
  @IsString()
  session_id?: string;
}

@ApiTags('agents')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller()
export class AgentsController {
  constructor(private readonly router: AgentRouterService) {}

  @Get()
  @ApiOperation({ summary: 'List all registered agents' })
  list() {
    return { agents: this.router.listAgents() };
  }

  @Post(':agentKey/invoke')
  @ApiOperation({ summary: 'Invoke a specific agent' })
  async invoke(
    @Param('agentKey') agentKey: string,
    @Body() dto: InvokeDto,
    @Req() req: { headers: { authorization?: string } },
  ) {
    if (!(agentKey in AGENT_REGISTRY)) {
      return { error: `Unknown agent: ${agentKey}` };
    }
    const token = req.headers.authorization?.replace('Bearer ', '') || '';
    return this.router.invoke(agentKey as keyof typeof AGENT_REGISTRY, dto, token);
  }
}
