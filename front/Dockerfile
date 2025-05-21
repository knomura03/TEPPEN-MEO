# 1. Node.jsの公式イメージをベースイメージとして使用します。
# LTS (Long Term Support) バージョンを指定するのが一般的です。
FROM node:20-alpine AS base

# pnpmをグローバルにインストールします。
RUN npm install -g pnpm

# 依存解決・ビルド用ステージ
FROM base AS builder
WORKDIR /app

# 依存解決に必要なファイルを先にコピー
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY front/package.json ./front/package.json

# 依存解決（ワークスペースルートで実行）
RUN pnpm install --frozen-lockfile

# ソースコード全体をコピー
COPY front/ ./front/

WORKDIR /app/front
RUN pnpm build

# 本番用ステージ
FROM base AS runner
WORKDIR /app/front
ENV NODE_ENV=production

COPY --from=builder /app/front/public ./public
COPY --from=builder /app/front/.next/standalone ./
COPY --from=builder /app/front/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"] 