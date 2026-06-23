import { Module } from '@nestjs/common';
import { ThrottlerModule } from '@nestjs/throttler';
import { AuthModule } from './auth/auth.module';
import { HealthModule } from './health/health.module';
import { ProxyModule } from './proxy/proxy.module';
import { VesselsModule } from './routes/vessels.module';
import { ContainersModule } from './routes/containers.module';
import { CustomsModule } from './routes/customs.module';
import { BillingModule } from './routes/billing.module';
import { AnalyticsModule } from './routes/analytics.module';

@Module({
  imports: [
    ThrottlerModule.forRoot([{ ttl: 60000, limit: 100 }]),
    AuthModule,
    HealthModule,
    ProxyModule,
    VesselsModule,
    ContainersModule,
    CustomsModule,
    BillingModule,
    AnalyticsModule,
  ],
})
export class AppModule {}
