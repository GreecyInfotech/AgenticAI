import { Controller, Get, UseGuards } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';

@ApiTags('billing')
@ApiBearerAuth()
@UseGuards(AuthGuard('jwt'))
@Controller('billing')
export class BillingController {
  @Get('invoices')
  invoices() {
    return {
      data: [
        { id: 'INV-001', customer: 'MSC', amount: 125000, status: 'paid', currency: 'USD' },
        { id: 'INV-002', customer: 'Maersk', amount: 89000, status: 'pending', currency: 'USD' },
      ],
      total: 2,
    };
  }

  @Get('revenue/summary')
  revenueSummary() {
    return { mtd: 2_450_000, ytd: 28_700_000, currency: 'USD', growth_pct: 8.3 };
  }
}
