import { IsString, MinLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class LoginDto {
  @ApiProperty({ example: 'operator' })
  @IsString()
  username!: string;

  @ApiProperty({ example: 'operator' })
  @IsString()
  @MinLength(1)
  password!: string;
}
