---

project: TEPPEN MEO
owner: 野村 克也
sprint: 2025-05-20 〜 2025-06-02
version: 0.6.0   # detailed with explanations
---------------------------------------------

# Dev TODO Board

## Status Legend

| Status | Description |
| ------ | ----------- |
| [ ]    | 未着手      |
| [~]    | 進行中      |
| [x]    | 完了        |
| [!]    | 問題あり    |
| DROP   | 中止        |

## タスクの優先順位付け
   - 🔴 緊急
   - 🟡 重要
   - 🟢 通常
   - ⚪ 低優先

更新ルール

1. 1 行＝1 タスク（2 日以内に完結する粒度が理想）。
2. ステータスは行頭キーワードを変更するだけ。
3. 各タスクの直下に「目的・完了条件」を 1 行で記載。
4. 原則として1行ずつ実行する。
5. 実行後は必ずステータスを更新し、行を追加してコメントを残す。（コメントに実行時の日時は不要）

---

## TODO

### 0. プロジェクト初期セットアップ

* [x] 🔴 | **リポジトリ初期化（Next.js + FastAPI モノレポ）**
  * 目的・完了条件: GitHub に空リポ作成後、`front/` と `backend/` を配置し `pnpm-workspace.yaml` で統合する。
  * 2025-05-21 完了: pnpmワークスペース・ルートpackage.json・front/backend/初期化・依存解決・ビルドまで全て正常動作
* [x] 🔴 | **CI/CD ベースライン（GitHub Actions）**
  * 目的・完了条件: `lint → test → build → deploy` の 4 ジョブを作り、PR 時に Vercel Preview URL を自動コメント。
  * 2025-05-21 完了: .github/workflows/ci.ymlを新規作成し、pnpmワークスペース対応のlint/test/build/Vercel Preview自動コメントまで自動化済み
* [x] 🔴 | **Docker Compose によるローカル統合環境**
  * 目的・完了条件: `docker compose up` で front+api+db+redis+celery が起動し、`http://localhost:3000` でアプリが閲覧できる状態にする。
  * 2025-05-21 完了: docker compose up --build で全サービス起動・Next.js/Poetry依存解決エラーも解消
* [x] 🟡 | **docs/architecture.md 雛形作成**
  * 目的・完了条件: C4モデルの System/Container 図＋矢印でデータフローを示し、更新が容易な状態を作る。
  * コメント: C4モデルの雛形として、System Context図、Container図、Component図のMermaid.js記述とデータフローのプレースホルダーを含むarchitecture.mdを作成しました。
* [~] 🟡 | **テーブル定義（users / oauth_tokens）**
  * 目的・完了条件: ER図作成→Alembicマイグレーション作成→pytestでCRUDを確認。
  * コメント: docs/db_schema.md にER図とテーブル定義を記述。backend/src/backend/models/ にUser, OAuthTokenモデル及び関連ファイルを作成。Alembic設定ファイル(alembic.ini, alembic/env.py)を作成し、マイグレーション生成の準備完了。
* [x] 🔴 | backend Dockerfile / docker-compose 修正
  * 目的・完了条件: Poetry不要で起動、.venvを維持し `uvicorn` が直接動作する。
  * 2025-05-21 完了: docker-compose.yml 修正（code-only volume, command変更）で backend コンテナ正常起動
* [~] 🔴 | Vercel シークレット登録
  * 目的・完了条件: GitHub リポに Vercel 用シークレット3種を登録し、Pull Request で Preview URL がコメントされる。
  * 2025-05-21 進行中: シークレット値の取得・設定手順を整備中

---

### 1. Setup & Infrastructure

* **クラウド基盤**
  * [ ] 🔴 | Vercel プロジェクト作成
    * 目的・完了条件: GitHub リポをリンクし、Vercel に `main` ブランチが push されたら自動デプロイされることを確認。
  * [ ] 🔴 | AWS IAM 初期ロール設計
    * 目的・完了条件: `AppRunnerDeployRole` に最小限の ECR/S3/RDS 権限を付与し、開発者用 IAM ユーザーを作成。
  * [ ] 🟡 | Route 53 ドメイン登録
    * 目的・完了条件: `teppen-meo.com` を取得し、ALIAS で Vercel / CloudFront に向ける。
* **ストレージ & ネットワーク**
  * [ ] 🟡 | S3 バケット作成（assets-teppen-meo）
    * 目的・完了条件: Public Block ON、CORS 設定 → presigned URL で画像アップロード可能にする。
  * [ ] 🟢 | CloudFront CDN 配置
    * 目的・完了条件: エッジロケーションを利用し、日本近郊のレスポンスを 50% 以上短縮する。
* **データベース & キャッシュ**
  * [ ] 🔴 | RDS PostgreSQL dev 構築
    * 目的・完了条件: パラメータ `max_connections=200`、自動バックアップ 7 日、秘密鍵接続を有効。
  * [ ] 🔴 | Elasticache Redis dev 構築
    * 目的・完了条件: `redis6.x` single node、`appendonly no` でパフォーマンス優先の設定。
* **コンテナサービス**
  * [ ] 🟡 | App Runner api-dev サービス
    * 目的・完了条件: Dockerfile ビルド→Auto deploy、ヘルスチェック `/health` が 200 を返すことを確認。
  * [ ] 🟡 | Fargate celery-worker タスク定義
    * 目的・完了条件: `concurrency=4`、ログを CloudWatch に送信し、失敗時に 3 回自動再起動を設定。
  * [ ] 🟢 | EventBridge Scheduler celery-beat
    * 目的・完了条件: `rate(5 minutes)` で HTTP invoke → worker の `/beat` エンドポイントを呼び出す。
* **セキュリティ & IaC**
  * [ ] 🟡 | GuardDuty 有効化
    * 目的・完了条件: すべてのリージョンで有効にし、High Severity Finding を Slack へ通知。
  * [ ] 🟢 | Terraform ベースライン（S3 state）
    * 目的・完了条件: `backend \"s3\"` を設定し、CI で `terraform fmt validate plan` を実行。

### 2. Frontend Foundation

* **プロジェクトスキャフォルド**
  * [x] 🔴 | create-next-app 導入
    * 目的・完了条件: `--tailwind --eslint --import-alias "@/*"` を付けて生成し、動作を確認。
    * 2025-05-21 完了: front/ ディレクトリにNext.jsプロジェクト生成済み
  * [x] 🔴 | Tailwind CSS + PostCSS 設定
    * 目的・完了条件: `tailwind.config.ts` に custom color token と `radix-colors` を統合。
    * 2025-05-21 完了: front/にtailwindcss, postcss, tailwind.config.ts, postcss.config.mjs等が存在
* **開発ツール**
  * [ ] 🟡 | ESLint + Prettier 設定
    * 目的・完了条件: `eslint-config-next`, `@typescript-eslint` をベースに VSCode 自動保存フォーマットを設定。
  * [ ] 🟢 | web-vitals 実装
    * 目的・完了条件: `_app.tsx` で `reportWebVitals` を実装し GA4 へ送る関数を作る。
* **ステート & 通信**
  * [ ] 🟡 | TanStack Query セットアップ
    * 目的・完了条件: `staleTime=30_000`, `retry=2`、API error を toast 表示。
  * [ ] 🟡 | Zustand グローバルステート基盤
    * 目的・完了条件: `useAuthStore`, `useUiStore` を作成し、型安全な selector を提供。
* **UI ライブラリ**
  * [ ] 🟡 | shadcn/ui インストール
    * 目的・完了条件: Button/Card/Dialog を scaffold。デフォルト `xl` ラディウスに変更。
  * [ ] 🟢 | i18n 基盤（react-intl）
    * 目的・完了条件: `LocaleSwitcher` コンポーネントを `/components/common` に追加。
* **PWA & メタ**
  * [ ] 🟢 | PWA マニフェスト草稿
    * 目的・完了条件: `next-pwa` を dev でもオフライン対応し、`start_url=\"/\"` を設定。
  * [ ] 🟢 | favicon / OG Image 生成
    * 目的・完了条件: `@vercel/og` を使って動的 OG 画像エンドポイントを作成。

### 3. Backend Foundation

* **FastAPI 基盤**
  * [x] 🔴 | poetry new backend プロジェクト
    * 目的・完了条件: `src/backend/__init__.py` を作成しパッケージ化。
    * 2025-05-21 完了: backend/ディレクトリにPoetryプロジェクト初期化済み
  * [x] 🔴 | FastAPI /health エンドポイント
    * 目的・完了条件: `return {"status":"ok","version":os.getenv('VERSION')}` を返す。
    * 2025-05-21 完了: src/backend/main.pyに/healthエンドポイント実装済み
  * [ ] 🟡 | Uvicorn 起動スクリプト
    * 目的・完了条件: `ENTRYPOINT [\"uvicorn\",\"backend.main:app\",\"--host\",\"0.0.0.0\",\"--port\",\"8000\",\"--workers\",\"4\"]` を Dockerfile に記述。
* **共通ライブラリ**
  * [ ] 🟡 | Logging (structlog) 設定
    * 目的・完了条件: `structlog.processors.TimeStamper(fmt=\"iso\")` を入れ JSON ログを整形。
  * [ ] 🟡 | pydantic v2 設定
    * 目的・完了条件: `model_config = {\"from_attributes\":True}` を BaseModel に共通化。
* **DB & マイグレーション**
  * [ ] 🔴 | SQLAlchemy Core セッション管理
    * 目的・完了条件: `async_sessionmaker` を DI し、トランザクションを contextmanager で扱う。
  * [ ] 🔴 | Alembic 初期化
    * 目的・完了条件: `alembic revision --autogenerate -m \"baseline\"` を実行し、DB とモデルが一致。
* **非同期処理**
  * [ ] 🟡 | Celery + Redis ブローカー設定
    * 目的・完了条件: Task serializer を `orjson`; visibility timeout を 3600 秒に設定。
* **テスト基盤**
  * [ ] 🟡 | pytest + Ruff + MyPy サンプルテスト
    * 目的・完了条件: `pytest --asyncio-mode=strict`、クラウド CI で `mypy --strict` を通す。

### 4. Authentication

* **NextAuth.js**
  * [ ] 🔴 | Credentials Provider 実装
    * 目的・完了条件: `/api/auth/callback/credentials` で bcrypt 検証し、JWT を返却する。
  * [ ] 🟡 | Google OAuth Provider 追加 (Googleビジネスプロフィール連携用)
    * 目的・完了条件: GCP OAuth 同意画面に `business.manage` scope を追加し、レビュー提出。レビュー期間を考慮し早めに着手。
  * [ ] 🟡 | Facebook OAuth Provider 追加 (Facebookページ・Instagram連携用)
    * 目的・完了条件: Meta App を「ライブ」状態にし、`instagram_basic, pages_manage_posts, pages_read_engagement, pages_messaging` 権限を production モードで許可。レビュー期間を考慮し早めに着手。
* **Token 戦略**
  * [ ] 🟡 | JWT access/refresh 実装
    * 目的・完了条件: refresh トークンは httpOnly cookie に保存し、`/auth/refresh` でローテーション。
  * [ ] 🟢 | OAuth トークン永続化テーブル
    * 目的・完了条件: 失効トークンは定期クーロンで削除し、警告メールを送信。
* **UX**
  * [ ] 🟡 | 初回オンボーディング画面
    * 目的・完了条件: 店舗名・住所・カテゴリを入力し Google / Facebook 連携を促すステップフォーム。UIデザイン確定後、実装。
  * [ ] 🟢 | パスワードリセット（AWS SES）
    * 目的・完了条件: `/api/auth/forgot` → 一意トークンを発行し、SES テンプレートメールを送信。
  * [ ] ⚪ | 二段階認証 (TOTP) 検討・導入判断
    * 目的・完了条件: セキュリティ要件とユーザビリティを考慮し、TOTP導入の是非を判断。導入する場合、`speakeasy`等ライブラリでQRコード生成し、ユーザーが任意で設定できる機能として実装。MVPリリース後の追加機能としても検討可。

### 5. Posting MVP (一括投稿・スケジュール投稿含む)

* **テーブル定義**
  * [ ] 🔴 | posts テーブル設計
    * 目的・完了条件: `id, user_id, caption, image_urls[ARRAY], video_urls[ARRAY], platforms[ARRAY], scheduled_at, status ENUM(draft, scheduled, posted, failed, canceled), error_message` を持ち、`user_id, scheduled_at` にインデックス。
* **外部 API ラッパー**
  * [ ] 🔴 | Instagram Graph API (投稿・メディア管理)
    * 目的・完了条件: `/media` & `/media_publish` (画像・動画対応、リール投稿も含む) を httpx async ラッパーで実装し、rate-limit 429 をハンドリング。
  * [ ] 🔴 | Google Business Profile (GBP) Local Posts API
    * 目的・完了条件: `locations/{locationId}/localPosts` エンドポイントに POST (イベント、オファー、最新情報)、レスポンス ID を保存。画像・動画対応。
  * [ ] 🟡 | Facebook Graph API (ページ投稿)
    * 目的・完了条件: `/{page-id}/feed` または `/{page-id}/photos`, `/{page-id}/videos` エンドポイントに httpx async ラッパーで投稿。rate-limit対応。
* **ファイル & 画像処理**
  * [ ] 🟡 | 画像・動画アップロード presigned URL (S3)
    * 目的・完了条件: `/api/upload` を作成し、S3 への PUT URL を発行。コンテンツタイプ、サイズ制限を設定。
  * [ ] 🟢 | 画像トリミング・動画プレビュー
    * 目的・完了条件: `react-easy-crop` 等で画像トリミング。動画は `<video>` タグでプレビュー。各プラットフォームの推奨アスペクト比に対応。
* **バッチ処理 (スケジュール投稿・一括投稿)**
  * [ ] 🔴 | Celery batch_post タスク (スケジュール・一括投稿処理)
    * 目的・完了条件: `eta=scheduled_at` で遅延実行。複数プラットフォーム・複数投稿を asyncio.gather で並列投稿。部分的な失敗もハンドリング。
  * [ ] 🟡 | 投稿ステータス更新・エラー通知
    * 目的・完了条件: 投稿完了/失敗時にDBステータス更新。失敗時はユーザーに通知（UI上およびメール等）。
  * [ ] 🟢 | レート制御 Semaphore (プラットフォーム毎)
    * 目的・完了条件: 各プラットフォームAPIのレート制限に基づき、`asyncio.Semaphore` 等で並列実行数を制御。
* **UI (投稿管理画面)**
  * [ ] 🟡 | 投稿作成・編集フォーム UI
    * 目的・完了条件: 各プラットフォーム向けカスタマイズ項目（例：GBPのCTAボタン）、キャプション (ハッシュタグサジェスト、文字数カウンタ)、画像・動画アップローダー、プレビュー、スケジュール設定。
  * [ ] 🟡 | 投稿カレンダー表示・一覧テーブル UI
    * 目的・完了条件: カレンダー形式での投稿スケジュール表示。`DataTable` で status / platform / scheduled_at / プレビュー等を表示。
  * [ ] 🟢 | 投稿フィルタ・ソート機能
    * 目的・完了条件: TanStack Table でステータス、プラットフォーム、日付範囲等でフィルタリング。投稿日時等でソート。
  * [ ] 🟢 | 投稿キャンセル・再試行機能
    * 目的・完了条件: status が `scheduled` または `failed` の投稿をキャンセルまたは再試行可能に。Celeryタスクのrevoke/再実行。
  * [ ] ⚪ | 投稿テンプレート保存・呼び出し機能
    * 目的・完了条件: よく使う投稿内容をテンプレートとして保存し、新規投稿時に呼び出せるようにする。
  * [ ] ⚪ | 投稿エクスポート CSV
    * 目的・完了条件: `/api/posts/export?from=...&to=...` でダウンロード可能に。

### 6. DM Management MVP (一元管理)

* **データモデル**
  * [ ] 🔴 | dm_threads / dm_messages テーブル
    * 目的・完了条件: thread_id, platform (Instagram, Facebook), external_thread_id, user_id, last_message_at, unread_count, snippet 等を保持。全文検索用にGINインデックス。
* **API 同期 (バックグラウンド処理)**
  * [ ] 🔴 | Facebook Messenger API 同期タスク (Webhook & 定期ポーリング)
    * 目的・完了条件: Webhook (`messages` サブスクリプション) でリアルタイム受信。定期的に `/conversations` → `/messages` をページネーションし差分取得。
  * [ ] 🔴 | Instagram Direct Message API 同期タスク (Webhook & 定期ポーリング)
    * 目的・完了条件: Webhook (`messages` サブスクリプション) でリアルタイム受信。Graph API `/{user-id}/conversations` を利用し差分取得。
  * [ ] 🟡 | Googleビジネスプロフィール メッセージ機能調査・実装
    * 目的・完了条件: GBP APIドキュメントでメッセージ送受信に関するAPIエンドポイントの有無と仕様を詳細調査。公式APIが存在すれば同期タスクを実装。存在しない場合は代替手段（例：メール通知連携など）を検討・提案。
* **フロント UI (DM管理画面)**
  * [ ] 🟡 | DMスレッド一覧（無限スクロール、フィルタ）
    * 目的・完了条件: プラットフォーム別、未読/既読、担当者等でフィルタ。IntersectionObserverで無限スクロール。ローディングスケルトン。
  * [ ] 🟡 | スレッド詳細表示 + 返信フォーム UI
    * 目的・完了条件: 右側パネルでスレッドを展開。画像・定型文添付、Enter送信/Shift+Enter改行。相手の既読ステータス表示。
  * [ ] 🟡 | 未読バッジ・既読処理 (API連携)
    * 目的・完了条件: スレッド開封時に既読APIを呼び出し、UIバッジを即時消去。Webhook等でリアルタイムに未読数を更新。
  * [ ] 🟢 | DM内検索機能 (メッセージ本文)
    * 目的・完了条件: PostgreSQLの全文検索機能を利用し、スレッド横断でメッセージ本文を検索。
  * [ ] ⚪ | DM担当者割り当て機能 (MVPリリース後の検討)
    * 目的・完了条件: 各スレッドに担当者を割り当て、チームでの対応を効率化する機能。MVPリリース後の優先度で検討。
  * [ ] ⚪ | 定型文返信機能 (MVPリリース後の検討)
    * 目的・完了条件: よく使う返信文をカテゴリ別に登録し、DM返信時に簡単に呼び出せる機能。MVPリリース後の優先度で検討。

### 7. Review Management MVP (クチコミ管理・返信)

* **クチコミ取得 (バックグラウンド処理)**
  * [ ] 🔴 | Google Business Profile (GBP) Reviews API
    * 目的・完了条件: `accounts/{accountId}/locations/{locationId}/reviews` で star, comment, updateTime, reviewer_name, reviewer_icon 等を取得。返信もAPI経由で。
  * [ ] 🟡 | Facebookページ クチコミ (推奨) API
    * 目的・完了条件: Facebook Graph API `/{page-id}/ratings` または関連エンドポイントでクチコミと評価を取得。
  * [ ] 🟢 | Instagram コメント監視・クチコミとしての取り込み判断
    * 目的・完了条件: 投稿へのコメントを定期的に取得。クチコミとして管理画面に取り込むか（キーワードフィルタリング等）、別途コメント管理機能とするか仕様を決定。MVPでは表示のみに留めることも検討。
* **データモデル & 同期**
  * [ ] 🔴 | reviews テーブル設計
    * 目的・完了条件: `review_id, external_review_id, location_id (FK to user_platform_connections), platform, rating, comment, reviewer_name, review_url, replied_at, reply_content, status ENUM(new, replied, archived), sentiment`。UNIQUE(external_review_id, platform)。
  * [ ] 🟡 | Review 同期 Celery タスク (各プラットフォーム)
    * 目的・完了条件: 1時間ごとに最新クチコミを差分保存。新規/更新クチコミは通知対象。
* **UI & 返信機能 (クチコミ管理画面)**
  * [ ] 🟡 | クチコミ一覧・フィルタUI
    * 目的・完了条件: プラットフォーム別、評価(星)別、返信状況別、期間別フィルタ。未返信を優先表示。
  * [ ] 🟡 | クチコミ返信フォーム UI (各プラットフォームAPI連携)
    * 目的・完了条件: クチコミ詳細画面から直接返信。返信内容はDBにも保存。
  * [ ] 🟢 | 返信テンプレート機能
    * 目的・完了条件: ポジティブ/ネガティブ評価など状況に応じた返信テンプレートを複数保存・呼び出し可能に。
* **分析 & 通知**
  * [ ] 🟢 | Sentiment 分析（無料OSSモデル優先で調査・選定）
    * 目的・完了条件: クチコミ本文から感情分析 (positive/neutral/negative) を行いDBに保存。日本語対応の無料OSSモデル（例：GiNZA, SudachiTra等と連携可能なモデル）を優先的に調査・選定。精度と運用コストを比較検討。
  * [ ] 🟢 | ネガティブレビュー・特定キーワード通知 (Slack/メール)
    * 目的・完了条件: 低評価 (例: 星2以下) や特定キーワード (例: 「問題」「不満」) を含むクチコミ受信時に即時通知。
  * [ ] ⚪ | クチコミ CSV エクスポート
    * 目的・完了条件: 管理画面から期間・プラットフォーム指定でクチコミデータをCSVダウンロード。

### 8. Competitor Analytics MVP (競合分析)

* **データ収集・管理**
  * [ ] 🟡 | competitors テーブル設計
    * 目的・完了条件: `competitor_id, user_id (FK), name, gbp_place_id, ig_username, fb_page_id, notes`。ユーザーが競合を複数登録可能。(Yahooプレイス関連フィールドは一旦削除)
  * [ ] 🟡 | 競合GBP情報収集タスク (公開情報ベース)
    * 目的・完了条件: 競合のGBPリスティングから評価、クチコミ数、写真数などを定期的にスクレイピングまたは手動入力支援UI。
  * [ ] 🟡 | 競合Instagram情報収集タスク (公開情報ベース)
    * 目的・完了条件: 競合の公開Instagramプロフィールからフォロワー数、投稿数、投稿エンゲージメント（いいね・コメント数）などをAPI制限に注意しつつ定期的にスクレイピング。
  * [ ] 🟢 | 競合Facebookページ情報収集タスク (公開情報ベース)
    * 目的・完了条件: 競合の公開Facebookページから「いいね！」数、フォロワー数、投稿エンゲージメントなどをAPI制限に注意しつつ定期的にスクレイピング。
* **可視化 & レポート (分析画面)**
  * [ ] 🟡 | Recharts等を用いた競合比較グラフ
    * 目的・完了条件: クチコミ数、評価平均、フォロワー数などの主要指標を自店舗と競合で比較する時系列グラフ（LineChart, BarChart）。
  * [ ] 🟢 | 主要KPIレーダーチャート
    * 目的・完了条件: クチコミ評価、投稿頻度、フォロワー数などの複数KPIをレーダーチャートで総合比較。
  * [ ] 🟢 | KPIスコアカード表示
    * 目的・完了条件: 主要指標について、競合平均との比較で自店舗の優位性を色分け表示（例: 赤・黄・緑）。
  * [ ] ⚪ | 競合の最新投稿・クチコミ表示 (可能な範囲で)
    * 目的・完了条件: 競合の最新の公開投稿やクチコミを一部表示し、動向を把握しやすくする。
  * [ ] ⚪ | 週次/月次競合比較レポート生成判断 (MVPリリース後の検討)
    * 目的・完了条件: `reportlab`等でのPDFレポート生成、またはメールでのサマリー送信機能の要否を判断。MVPリリース後の優先度で検討。

### 9. Platform Settings & Management (各種設定)

* [ ] 🟡 | **アカウント連携管理画面 UI**
  * 目的・完了条件: Google、Facebook (Instagram含む) との連携状況を表示。連携追加・解除機能。(Yahooプレイス連携は将来対応)
* [ ] 🟡 | **店舗情報管理フォーム UI**
  * 目的・完了条件: 各プラットフォームに共通する基本店舗情報（店名、住所、電話番号、営業時間、カテゴリ等）を一元管理・更新。プラットフォーム固有項目も設定可能に。
* [ ] 🟢 | **通知設定画面 UI**
  * 目的・完了条件: 新規DM、新規クチコミ、投稿失敗などのイベント毎に通知（メール、アプリ内通知）のオンオフを設定可能に。
* [ ] 🟢 | **ユーザ管理・権限設定 (MVPではオーナーのみ)**
    * 目的・完了条件: MVPでは単一オーナーアカウントのみを想定。将来的なチーム利用（編集者、閲覧者ロールなど）のための拡張性を考慮した設計に留める。
* [ ] ⚪ | **請求・プラン管理画面 (将来対応)**
    * 目的・完了条件: Stripe等の決済サービスと連携し、利用プランの確認・変更、支払い履歴の表示など。ローンチ後の機能として計画。

### 10. Testing & Quality

* **フロントテスト**
  * [ ] 🟡 | React Testing Library セットアップと基本テスト
    * 目的・完了条件: `jest` + `@testing-library/jest-dom`。主要コンポーネントのユニットテスト・スナップショットテスト作成。
  * [ ] 🟢 | Playwright E2Eテスト (主要シナリオ)
    * 目的・完了条件: `シナリオ: ログイン → 投稿作成 → スケジュール設定 → DM確認 → クチコミ返信` などをCIでヘッドレス実行。
* **バックエンドテスト**
  * [ ] 🟡 | PytestによるAPIユニットテスト・統合テスト
    * 目的・完了条件: 主要APIエンドポイントのテストケース作成。DBモック、外部APIモック活用。カバレッジ80%以上目標。
  * [ ] ⚪ | Mutation Testing (pytest-muter) 導入検討 (MVPリリース後)
    * 目的・完了条件: 目標サバイバル率 <20% として品質向上に寄与するか、MVPリリース後に評価・検討。
* **品質ゲート**
  * [ ] 🟢 | SVG/PNG スナップショット CI (無料ツール優先で調査・選定)
    * 目的・完了条件: UIコンポーネントの視覚的回帰テスト。無料または低コストで利用可能なツール（例: Playwrightのビジュアル比較、Storybookアドオン等）を調査・選定しCIに組み込む。
  * [ ] 🟢 | Lighthouse CIによるパフォーマンスチェック
    * 目的・完了条件: PR時に主要ページのPerformanceスコア >= 80を要求。
  * [ ] ⚪ | OWASP ZAP 等によるセキュリティスキャン検討 (MVPリリース後)
    * 目的・完了条件: 定期的な自動スキャンを実行し、脆弱性を検出。MVPリリース後にツールの選定と導入を検討。

### 11. General UI/UX Improvements

* [ ] 🟡 | **ダッシュボード画面 MVP**
    * 目的・完了条件: ログイン後最初に表示される画面。主要KPI（未読DM数、未返信レビュー数、今日の投稿予定など）のスナップショット、よく使う機能へのショートカットを表示。UIデザイン確定後、実装。
* [ ] 🟢 | **レスポンシブデザイン対応**
  * 目的・完了条件: 主要画面がスマートフォン、タブレットでも適切に表示・操作できるようにTailwind CSSのブレークポイントを活用。
* [ ] 🟢 | **アクセシビリティ向上 (WCAG準拠意識)**
  * 目的・完了条件: キーボード操作、スクリーンリーダー対応、コントラスト比などに配慮したUI実装。
* [ ] ⚪ | **ダークモード対応検討 (MVPリリース後)**
    * 目的・完了条件: OS設定に連動または手動切り替えでダークモードを提供。shadcn/uiのテーマ機能活用。MVPリリース後の優先度で検討。

---
