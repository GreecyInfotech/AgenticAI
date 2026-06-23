import { Module } from '@nestjs/common';
import { ContainersController } from './containers.controller';

@Module({ controllers: [ContainersController] })
export class ContainersModule {}
