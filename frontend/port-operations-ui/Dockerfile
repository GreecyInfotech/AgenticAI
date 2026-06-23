FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY frontend/port-operations-ui/package.json ./frontend/port-operations-ui/
COPY shared/typescript/smart-port-types/package.json ./shared/typescript/smart-port-types/
RUN pnpm install --filter port-operations-ui...
COPY frontend/port-operations-ui ./frontend/port-operations-ui
COPY shared/typescript/smart-port-types ./shared/typescript/smart-port-types
RUN pnpm --filter port-operations-ui build

FROM nginx:alpine
COPY --from=builder /app/frontend/port-operations-ui/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
