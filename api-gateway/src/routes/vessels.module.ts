import { Module } from '@nestjs/common';
import { VesselsController } from './vessels.controller';

@Module({ controllers: [VesselsController] })
export class VesselsModule {}
