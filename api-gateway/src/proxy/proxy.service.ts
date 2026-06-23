import { Injectable } from '@nestjs/common';
import { createProxyMiddleware } from 'http-proxy-middleware';

export interface ServiceRoute {
  path: string;
  target: string;
  rewrite?: Record<string, string>;
}

@Injectable()
export class ProxyService {
  private readonly routes: ServiceRoute[] = [
    { path: '/agents/vessel', target: 'http://vessel-agent:8100' },
    { path: '/agents/container', target: 'http://container-agent:8101' },
    { path: '/agents/customs', target: 'http://customs-agent:8102' },
    { path: '/agents/billing', target: 'http://billing-agent:8103' },
    { path: '/agents/maintenance', target: 'http://maintenance-agent:8104' },
    { path: '/agents/incident', target: 'http://incident-agent:8105' },
    { path: '/agents/planning', target: 'http://planning-agent:8106' },
    { path: '/agents/safety', target: 'http://safety-agent:8107' },
    { path: '/agents/weather', target: 'http://weather-agent:8108' },
    { path: '/agents/logistics', target: 'http://logistics-agent:8109' },
    { path: '/agents/executive', target: 'http://executive-agent:8110' },
    { path: '/ml/vessel-delay', target: 'http://vessel-delay-prediction:8300' },
    { path: '/ml/berth', target: 'http://berth-optimization:8301' },
    { path: '/ml/congestion', target: 'http://congestion-prediction:8304' },
    { path: '/rag/search', target: 'http://vector-search:8203' },
  ];

  getRoutes(): ServiceRoute[] {
    return this.routes;
  }

  createProxy(target: string) {
    return createProxyMiddleware({
      target,
      changeOrigin: true,
      pathRewrite: { '^/api/v1': '' },
    });
  }
}
