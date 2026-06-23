FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY frontend/customs-dashboard/package.json ./frontend/customs-dashboard/
COPY shared/typescript/smart-port-types/package.json ./shared/typescript/smart-port-types/
RUN pnpm install --filter customs-dashboard...
COPY frontend/customs-dashboard ./frontend/customs-dashboard
COPY shared/typescript/smart-port-types ./shared/typescript/smart-port-types
RUN pnpm --filter customs-dashboard build

FROM nginx:alpine
COPY --from=builder /app/frontend/customs-dashboard/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
