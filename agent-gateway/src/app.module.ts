import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { AgentsModule } from './agents/agents.module';
import { OrchestrationModule } from './orchestration/orchestration.module';
import { HealthModule } from './health/health.module';
import { JwtStrategy } from './auth/jwt.strategy';

@Module({
  imports: [
    PassportModule.register({ defaultStrategy: 'jwt' }),
    JwtModule.register({
      secret: process.env.JWT_SECRET || 'change-me-in-production',
      signOptions: { expiresIn: '24h' },
    }),
    AgentsModule,
    OrchestrationModule,
    HealthModule,
  ],
  providers: [JwtStrategy],
})
export class AppModule {}
