import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import helmet from 'helmet';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(helmet());
  app.enableCors({ origin: process.env.CORS_ORIGINS?.split(',') || ['*'] });
  app.setGlobalPrefix('agents/v1');
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));

  const config = new DocumentBuilder()
    .setTitle('Smart Port Agent Gateway')
    .setDescription('Orchestration gateway for multi-agent AI operations')
    .setVersion('1.0.0')
    .addBearerAuth()
    .build();
  SwaggerModule.setup('agents/docs', app, SwaggerModule.createDocument(app, config));

  const port = process.env.AGENT_GATEWAY_PORT || 8081;
  await app.listen(port);
  console.log(`Agent Gateway running on http://localhost:${port}`);
}

bootstrap();
