import { Controller, Get, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';

const MOCK_VESSELS = [
  { id: 'VSL-001', name: 'MSC Aurora', eta: '2026-06-24T08:00:00Z', berth: 'B-12', status: 'approaching' },
  { id: 'VSL-002', name: 'Maersk Horizon', eta: '2026-06-24T14:30:00Z', berth: 'B-08', status: 'scheduled' },
  { id: 'VSL-003', name: 'CMA CGM Pacific', eta: '2026-06-25T06:00:00Z', berth: 'B-15', status: 'scheduled' },
];

@ApiTags('vessels')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('vessels')
export class VesselsController {
  @Get()
  list() {
    return { data: MOCK_VESSELS, total: MOCK_VESSELS.length };
  }

  @Get('schedule')
  schedule() {
    return { data: MOCK_VESSELS, generated_at: new Date().toISOString() };
  }
}
