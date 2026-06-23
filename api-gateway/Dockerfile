FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY api-gateway/package.json ./api-gateway/
COPY shared/typescript/smart-port-types/package.json ./shared/typescript/smart-port-types/
RUN pnpm install --filter api-gateway...
COPY api-gateway ./api-gateway
COPY shared/typescript/smart-port-types ./shared/typescript/smart-port-types
RUN pnpm --filter api-gateway build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/api-gateway/dist ./dist
COPY --from=builder /app/api-gateway/package.json ./
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 8080
CMD ["node", "dist/main.js"]
