import { Controller, Get, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';

@ApiTags('containers')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('containers')
export class ContainersController {
  @Get()
  list() {
    return {
      data: [
        { id: 'CNTR-1001', type: '40HC', location: 'YARD-A-12', status: 'available' },
        { id: 'CNTR-1002', type: '20GP', location: 'YARD-B-05', status: 'in_transit' },
      ],
      total: 2,
    };
  }

  @Get('yard-status')
  yardStatus() {
    return { utilization: 0.78, total_slots: 5000, occupied: 3900, available: 1100 };
  }
}
