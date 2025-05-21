# Pythonの公式イメージをベースイメージとして使用します。
FROM python:3.11-slim AS base

# 環境変数の設定
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3

# pipをアップグレードし、Poetryをインストールします
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# 作業ディレクトリを設定します。
WORKDIR /app

# 依存関係インストール用のステージ
FROM base AS deps

# Poetryにプロジェクト内に仮想環境を作成するように指示します
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true

# pyproject.tomlの変更に合わせてpoetry.lockを更新（または生成）します。
# --no-interaction と --no-ansi はクリーンなログ出力のためです。
RUN poetry lock --no-update --no-interaction --no-ansi

# 依存関係をインストールします。
# --only main は本番用の依存関係のみをインストールします。
RUN poetry install --no-root --only main --no-interaction --no-ansi

# アプリケーション実行用のステージ
FROM python:3.11-slim AS runner
# python:3.11-slimを再度ベースにすることで、poetryやビルドツールが含まれない軽量なイメージにする

WORKDIR /app

# depsステージから仮想環境をコピーします
COPY --from=deps /app/.venv /app/.venv

# PATHに仮想環境のbinディレクトリを追加します
ENV PATH="/app/.venv/bin:$PATH"

# アプリケーションコードをコピーします。
# srcディレクトリのみをコピーし、main.pyなどがそこにあることを想定
COPY ./src /app/src

# FastAPIアプリケーションを起動するポートを公開します。
EXPOSE 8000

# アプリケーションを起動するコマンドです。
# poetry runは不要になり、直接uvicornをvenvから実行できる
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"] 