import { Module } from '@nestjs/common';
import { CustomsController } from './customs.controller';

@Module({ controllers: [CustomsController] })
export class CustomsModule {}
