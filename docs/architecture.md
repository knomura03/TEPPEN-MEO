# TEPPEN MEO システムアーキテクチャ

## 概要

このドキュメントは、TEPPEN MEOアプリケーションのアーキテクチャをC4モデルに基づいて記述したものです。

## 1. System Context Diagram (システムコンテキスト図)

TEPPEN MEO システムと外部システムとの関連を示します。

```mermaid
C4Context
  title System Context diagram for TEPPEN MEO

  Person(owner, "店舗オーナー", "TEPPEN MEOの主な利用者")
  System_Ext(google_b_api, "Google Business Profile API", "GBPの店舗情報、投稿、クチコミ管理")
  System_Ext(facebook_api, "Facebook Graph API", "Facebookページ及びInstagramアカウントの投稿、DM、クチコミ管理")
  System_Ext(s3, "AWS S3", "画像・動画ストレージ")
  System_Ext(vercel, "Vercel", "フロントエンドホスティング")
  System_Ext(aws_app_runner, "AWS App Runner", "バックエンドAPIホスティング")
  System_Ext(aws_rds, "AWS RDS (PostgreSQL)", "アプリケーションデータベース")
  System_Ext(aws_elasticache, "AWS ElastiCache (Redis)", "キャッシュ、Celeryブローカー")
  System_Ext(aws_fargate, "AWS Fargate", "Celeryワーカー実行環境")
  System_Ext(aws_eventbridge, "AWS EventBridge Scheduler", "Celery Beat (定期タスク実行)")

  System(teppen_meo, "TEPPEN MEO", "MEO対策・SNS一括管理ツール")

  Rel(owner, teppen_meo, "利用する")
  Rel(teppen_meo, google_b_api, "API連携")
  Rel(teppen_meo, facebook_api, "API連携")
  Rel(teppen_meo, s3, "画像・動画を保存/取得")
  Rel(teppen_meo, vercel, "フロントエンドをデプロイ")
  Rel(teppen_meo, aws_app_runner, "バックエンドAPIをデプロイ")
  Rel(teppen_meo, aws_rds, "データを永続化")
  Rel(teppen_meo, aws_elasticache, "キャッシュ/タスクキュー")
  Rel(teppen_meo, aws_fargate, "非同期タスクを実行")
  Rel(teppen_meo, aws_eventbridge, "定期タスクを起動")

  UpdateElementStyle(owner, $fontColor="white", $bgColor="rgb(0, 128, 0)")
  UpdateElementStyle(google_b_api, $fontColor="white", $bgColor="rgb(65,131,215)")
  UpdateElementStyle(facebook_api, $fontColor="white", $bgColor="rgb(59,89,152)")
```

### データフロー

*   店舗オーナーはTEPPEN MEOのフロントエンド（Vercel上でホスト）を通じてシステムを利用します。
*   TEPPEN MEOバックエンド（AWS App Runner上でホスト）は、Google Business Profile API、Facebook Graph APIと連携し、投稿、クチコミ、DMなどの情報を送受信します。
*   画像や動画はAWS S3に保存されます。
*   アプリケーションデータはAWS RDS (PostgreSQL) に永続化され、キャッシュやセッション情報はAWS ElastiCache (Redis) に保存されます。
*   非同期処理（スケジュール投稿、データ同期など）はCeleryワーカー (AWS Fargate) によって実行され、AWS EventBridge Schedulerが定期タスクをトリガーします。

## 2. Container Diagram (コンテナ図)

TEPPEN MEO システムを構成する主要なコンテナ（アプリケーション、データストアなど）を示します。

```mermaid
C4Container
  title Container diagram for TEPPEN MEO

  Person(owner, "店舗オーナー", "TEPPEN MEOの主な利用者")

  System_Ext(google_b_api, "Google Business Profile API", "GBPの店舗情報、投稿、クチコミ管理")
  System_Ext(facebook_api, "Facebook Graph API", "Facebookページ及びInstagramアカウントの投稿、DM、クチコミ管理")

  System_Boundary(c1, "TEPPEN MEO System") {
    Container(frontend, "Frontend (Next.js)", "TypeScript, Next.js, Tailwind CSS", "店舗オーナーが操作するWebインターフェース。Vercelでホスティング。")
    Container(backend_api, "Backend API (FastAPI)", "Python, FastAPI", "ビジネスロジック、外部API連携。AWS App Runnerでホスティング。")
    ContainerDb(database, "Database (PostgreSQL)", "AWS RDS", "ユーザー情報、投稿データ、クチコミ、DMなどを格納。")
    ContainerDb(cache_broker, "Cache & Message Broker (Redis)", "AWS ElastiCache", "APIレスポンスキャッシュ、セッションストア、Celeryタスクブローカー。")
    Container(s3_bucket, "Object Storage (S3)", "AWS S3", "投稿用の画像・動画ファイルストレージ。")
    Container(celery_worker, "Celery Worker", "Python, Celery", "非同期タスク（スケジュール投稿、データ同期など）を実行。AWS Fargateで実行。")
    Container(celery_beat, "Celery Beat Scheduler", "AWS EventBridge Scheduler", "定期的なタスク（データ収集など）を起動。")
  }

  Rel(owner, frontend, "HTTPS経由で利用")
  Rel(frontend, backend_api, "APIリクエスト (HTTPS/JSON)")

  Rel(backend_api, google_b_api, "APIリクエスト (HTTPS/JSON)")
  Rel(backend_api, facebook_api, "APIリクエスト (HTTPS/JSON)")
  Rel(backend_api, database, "データ読み書き (SQL)")
  Rel(backend_api, cache_broker, "キャッシュ読み書き、タスクエンキュー")
  Rel(backend_api, s3_bucket, "ファイルメタデータ管理、署名付きURL発行")

  Rel(celery_worker, backend_api, "内部API利用 (必要な場合)")
  Rel(celery_worker, google_b_api, "APIリクエスト (HTTPS/JSON)")
  Rel(celery_worker, facebook_api, "APIリクエスト (HTTPS/JSON)")
  Rel(celery_worker, database, "データ読み書き (SQL)")
  Rel(celery_worker, cache_broker, "タスクデキュー、結果保存")
  Rel(celery_worker, s3_bucket, "ファイル処理")

  Rel(celery_beat, celery_worker, "タスクをスケジュール (Redis経由)")


  UpdateElementStyle(owner, $fontColor="white", $bgColor="rgb(0, 128, 0)")
  UpdateElementStyle(frontend, $fontColor="white", $bgColor="rgb(27,114,208)")
  UpdateElementStyle(backend_api, $fontColor="white", $bgColor="rgb(40,167,69)")
  UpdateElementStyle(database, $fontColor="white", $bgColor="rgb(108,52,131)")
  UpdateElementStyle(cache_broker, $fontColor="white", $bgColor="rgb(217,83,79)")
  UpdateElementStyle(s3_bucket, $fontColor="white", $bgColor="rgb(240,173,78)")
  UpdateElementStyle(celery_worker, $fontColor="black", $bgColor="rgb(247,144,61)")
  UpdateElementStyle(celery_beat, $fontColor="black", $bgColor="rgb(91,192,222)")
```

### データフロー詳細 (例)

*   **投稿機能**:
    1.  店舗オーナーがフロントエンドで投稿内容を作成・スケジュール設定。
    2.  フロントエンドはバックエンドAPIに投稿データ（テキスト、S3上の画像/動画URL、スケジュール日時）を送信。
    3.  バックエンドAPIは投稿データをDBに保存し、スケジュール日時が未来であればCeleryタスクをRedisにエンキュー。
    4.  指定時刻になるとCelery BeatがCeleryワーカーを起動（またはFargate上のワーカーがRedisからタスクをデキュー）。
    5.  Celeryワーカーが各プラットフォームAPI（Google, Facebook/Instagram）に投稿を実行。
    6.  結果をDBに保存し、必要であればユーザーに通知。

*   **DM同期機能**:
    1.  (初回または定期) Celery BeatがDM同期タスクを起動。
    2.  CeleryワーカーがFacebook/Instagram APIにアクセスし、新しいメッセージを取得。
    3.  取得したメッセージをDBに保存。
    4.  店舗オーナーがフロントエンドでDM画面を開くと、バックエンドAPI経由でDBから最新DMを取得表示。
    5.  店舗オーナーが返信すると、バックエンドAPI経由で該当プラットフォームAPIに送信、DBも更新。


## 3. Component Diagram (コンポーネント図) - (オプション)

特定のコンテナ内の主要なコンポーネントとそのインタラクションを示します。 (必要に応じて作成)

例: Backend API のコンポーネント図

```mermaid
C4Component
  title Component diagram for Backend API

  Container(backend_api, "Backend API (FastAPI)") {
    Component(auth_module, "認証モジュール", "FastAPI Router", "ユーザー認証、トークン管理")
    Component(post_module, "投稿管理モジュール", "FastAPI Router", "投稿作成・編集・取得API")
    Component(dm_module, "DM管理モジュール", "FastAPI Router", "DM取得・送信API")
    Component(review_module, "クチコミ管理モジュール", "FastAPI Router", "クチコミ取得・返信API")
    Component(platform_service, "プラットフォーム連携サービス", "Python Module", "Google/Facebook APIラッパー")
    Component(db_service, "データベースサービス", "SQLAlchemy", "DBアクセス、ORM")
  }
  System_Ext(database, "Database (PostgreSQL)")
  System_Ext(google_b_api, "Google Business Profile API")
  System_Ext(facebook_api, "Facebook Graph API")

  Rel(auth_module, db_service, "ユーザー情報検証")
  Rel(post_module, db_service, "投稿データCRUD")
  Rel(post_module, platform_service, "外部プラットフォームへ投稿")
  Rel(dm_module, db_service, "DMデータCRUD")
  Rel(dm_module, platform_service, "外部プラットフォームとDM送受信")
  Rel(review_module, db_service, "クチコミデータCRUD")
  Rel(review_module, platform_service, "外部プラットフォームのクチコミ操作")

  Rel(platform_service, google_b_api, "APIコール")
  Rel(platform_service, facebook_api, "APIコール")
  Rel(db_service, database, "SQL実行")

```

## 4. Code Diagram (コード図) - (オプション)

特定のコンポーネントのクラス構造など、より詳細な実装レベルを示します。 (通常はアーキテクチャドキュメントでは省略)


## 更新履歴

*   YYYY-MM-DD: 初版作成 