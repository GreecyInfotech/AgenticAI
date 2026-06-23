import { Controller, Get, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';

@ApiTags('customs')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('customs')
export class CustomsController {
  @Get('declarations')
  declarations() {
    return {
      data: [
        { id: 'DEC-001', vessel: 'MSC Aurora', status: 'pending_review', risk_score: 0.2 },
        { id: 'DEC-002', vessel: 'Maersk Horizon', status: 'cleared', risk_score: 0.05 },
      ],
      total: 2,
    };
  }

  @Get('clearance-queue')
  queue() {
    return { pending: 12, in_review: 5, cleared_today: 28 };
  }
}
