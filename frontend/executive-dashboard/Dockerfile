FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY frontend/executive-dashboard/package.json ./frontend/executive-dashboard/
COPY shared/typescript/smart-port-types/package.json ./shared/typescript/smart-port-types/
RUN pnpm install --filter executive-dashboard...
COPY frontend/executive-dashboard ./frontend/executive-dashboard
COPY shared/typescript/smart-port-types ./shared/typescript/smart-port-types
RUN pnpm --filter executive-dashboard build

FROM nginx:alpine
COPY --from=builder /app/frontend/executive-dashboard/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
