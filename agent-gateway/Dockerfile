FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY agent-gateway/package.json ./agent-gateway/
COPY shared/typescript/smart-port-types/package.json ./shared/typescript/smart-port-types/
RUN pnpm install --filter agent-gateway...
COPY agent-gateway ./agent-gateway
COPY shared/typescript/smart-port-types ./shared/typescript/smart-port-types
RUN pnpm --filter agent-gateway build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/agent-gateway/dist ./dist
COPY --from=builder /app/agent-gateway/package.json ./
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 8081
CMD ["node", "dist/main.js"]
