# ChangeSet

## ChangeSet 名
- ID: changeset-1.2.1.1.2-backend-navigation-handlers
- 所属 Task: task-1.2.1.1-bucket-folder-navigation-api

## 変更対象
- backend/app/routes/s3.py
- backend/infrastructure/s3_gateway.py
- backend/tests/test_s3_routes.py

## ファイル一覧
※ 種別: Add / Modify / Delete

### backend/app/routes/s3.py
#### 1. バケット一覧ハンドラを追加
- 作業種別: Modify
- 目的: 認証/認可ガード下でバケット一覧を取得できるようにするため
- 変更内容: list_buckets_handler を追加し、auth_context 必須化と authorize_list_buckets 判定でフェイルクローズした上で list_buckets を呼び出す。continuation_token/limit を引数で受け取り下位関数へ渡す

#### 2. プレフィックス一覧ハンドラを追加
- 作業種別: Modify
- 目的: 認証/認可ガード下でプレフィックス一覧を取得できるようにするため
- 変更内容: list_prefixes_handler を追加し、auth_context 必須化と authorize_list_prefixes 判定でフェイルクローズした上で list_prefixes を呼び出す。bucket/prefix/continuation_token/limit を引数で受け取り下位関数へ渡す

### backend/infrastructure/s3_gateway.py
#### 1. バケット一覧の委譲関数を追加
- 作業種別: Modify
- 目的: 一覧取得の外部依存を関数注入で分離するため
- 変更内容: list_buckets を追加し、list_objects と同様に fetch_list_buckets を呼び出す(注入は呼び出し元で行う)

#### 2. プレフィックス一覧の委譲関数を追加
- 作業種別: Modify
- 目的: 一覧取得の外部依存を関数注入で分離するため
- 変更内容: list_prefixes を追加し、list_objects と同様に fetch_list_prefixes を呼び出す(注入は呼び出し元で行う)

### backend/tests/test_s3_routes.py
#### 1. 一覧ハンドラの正常/異常系テストを追加
- 作業種別: Add
- 目的: 認証/認可ガードとページング引数の受け渡しを保証するため
- 変更内容: list_buckets_handler/list_prefixes_handler で認証コンテキスト不在/認可失敗/認可成功の各ケースに加え、continuation_token/limit が下位関数へ渡ることを検証する
