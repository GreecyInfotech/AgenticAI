import { Controller, Get, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';

@ApiTags('analytics')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('analytics')
export class AnalyticsController {
  @Get('kpis')
  kpis() {
    return {
      vessel_calls_mtd: 142,
      teu_handled_mtd: 285000,
      avg_turnaround_hours: 18.5,
      gate_throughput_daily: 3200,
      crane_utilization_pct: 82.4,
      customs_clearance_rate_pct: 94.2,
      safety_incidents_mtd: 2,
      revenue_mtd_usd: 2_450_000,
    };
  }

  @Get('dashboard/executive')
  executiveDashboard() {
    return {
      kpis: {
        vessel_calls_mtd: 142,
        teu_handled_mtd: 285000,
        revenue_mtd_usd: 2_450_000,
        on_time_performance_pct: 91.2,
      },
      trends: {
        vessel_calls: [120, 128, 135, 142],
        revenue: [2.1, 2.2, 2.3, 2.45],
      },
    };
  }
}
