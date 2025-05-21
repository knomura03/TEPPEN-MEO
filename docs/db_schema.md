# データベーススキーマ (ER図)

## 概要

このドキュメントは、TEPPEN MEOアプリケーションの主要なデータベーステーブルの構造とリレーションシップを示します。

## ER図

```mermaid
erDiagram
    USERS {
        integer id PK "ユーザーID (主キー)"
        string email UNIQUE "メールアドレス (ユニーク)"
        string hashed_password "ハッシュ化されたパスワード"
        string full_name "氏名"
        boolean is_active "アクティブフラグ (デフォルト: true)"
        boolean is_superuser "スーパーユーザーフラグ (デフォルト: false)"
        datetime created_at "作成日時 (デフォルト: NOW())"
        datetime updated_at "更新日時 (デフォルト: NOW() ON UPDATE NOW())"
    }

    OAUTH_TOKENS {
        integer id PK "トークンID (主キー)"
        integer user_id FK "ユーザーID (USERS.idへの外部キー)"
        string provider "プロバイダー名 (例: google, facebook)"
        string access_token "アクセストークン"
        string refresh_token "リフレッシュトークン (オプション)"
        datetime expires_at "有効期限 (オプション)"
        string scopes "スコープ (スペース区切り、オプション)"
        datetime created_at "作成日時 (デフォルト: NOW())"
        datetime updated_at "更新日時 (デフォルト: NOW() ON UPDATE NOW())"
    }

    USERS ||--o{ OAUTH_TOKENS : "has"

```

## テーブル定義詳細

### `USERS` テーブル

TEPPEN MEOのユーザーアカウント情報を格納します。

*   `id`: 主キー、自動採番。
*   `email`: ログインに使用するメールアドレス。ユニーク制約。
*   `hashed_password`: bcrypt等でハッシュ化されたパスワード。
*   `full_name`: ユーザーの氏名または表示名。
*   `is_active`: アカウントが有効かどうかを示すフラグ。デフォルトは `true`。
*   `is_superuser`: 管理者権限を持つかどうかを示すフラグ。デフォルトは `false`。
*   `created_at`: レコード作成日時。
*   `updated_at`: レコード最終更新日時。

### `OAUTH_TOKENS` テーブル

ユーザーが連携した外部OAuthプロバイダー（Google、Facebookなど）のトークン情報を格納します。

*   `id`: 主キー、自動採番。
*   `user_id`: `USERS`テーブルの`id`への外部キー。どのユーザーのトークンかを示す。
*   `provider`: OAuthプロバイダー名（例: `google`, `facebook`）。
*   `access_token`: 外部APIへのアクセスに使用するアクセストークン。
*   `refresh_token`: アクセストークンを再取得するためのリフレッシュトークン（プロバイダーによる）。
*   `expires_at`: アクセストークンの有効期限。
*   `scopes`: このトークンに許可されたスコープ（権限範囲）。
*   `created_at`: レコード作成日時。
*   `updated_at`: レコード最終更新日時。 