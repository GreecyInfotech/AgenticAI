FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY frontend/mobile-app/package.json ./frontend/mobile-app/
COPY shared/typescript/smart-port-types/package.json ./shared/typescript/smart-port-types/
RUN pnpm install --filter mobile-app...
COPY frontend/mobile-app ./frontend/mobile-app
COPY shared/typescript/smart-port-types ./shared/typescript/smart-port-types
RUN pnpm --filter mobile-app build

FROM nginx:alpine
COPY --from=builder /app/frontend/mobile-app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
