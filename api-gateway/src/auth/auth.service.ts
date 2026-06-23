import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { LoginDto } from './dto/login.dto';

@Injectable()
export class AuthService {
  constructor(private readonly jwtService: JwtService) {}

  async login(dto: LoginDto) {
    // Production: integrate with Okta/Azure AD
    const users: Record<string, { password: string; roles: string[] }> = {
      admin: { password: 'admin', roles: ['admin', 'operator'] },
      operator: { password: 'operator', roles: ['operator'] },
      customs: { password: 'customs', roles: ['customs_officer'] },
      executive: { password: 'executive', roles: ['executive'] },
    };

    const user = users[dto.username];
    if (!user || user.password !== dto.password) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const payload = { sub: dto.username, email: `${dto.username}@smartport.io`, roles: user.roles };
    return {
      access_token: this.jwtService.sign(payload),
      token_type: 'Bearer',
      expires_in: 86400,
      user: { username: dto.username, roles: user.roles },
    };
  }

  validateToken(payload: { sub: string; email: string; roles: string[] }) {
    return { userId: payload.sub, email: payload.email, roles: payload.roles };
  }
}
