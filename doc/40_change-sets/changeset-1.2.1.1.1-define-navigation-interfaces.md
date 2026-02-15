# ChangeSet

## ChangeSet 名
- ID: changeset-1.2.1.1.1-define-navigation-interfaces
- 所属 Task: task-1.2.1.1-bucket-folder-navigation-api

## 変更対象
- doc/25_interfaces/open-api.yaml

## ファイル一覧
※ 種別: Add / Modify / Delete

### doc/25_interfaces/open-api.yaml
#### 1. バケット一覧 API を定義
- 作業種別: Add
- 目的: 一覧ナビゲーションの契約を明示するため
- 変更内容: HTTP GET /api/s3/buckets、Authorization ヘッダー必須、クエリ(continuation_token, limit)、レスポンス(buckets: [{name}], continuation_token)、エラー(401/403/500 と error: {code, message})を記載する

#### 2. プレフィックス一覧 API を定義
- 作業種別: Add
- 目的: フォルダ一覧の契約を明示するため
- 変更内容: HTTP GET /api/s3/prefixes、Authorization ヘッダー必須、クエリ(bucket, prefix, continuation_token, limit)、レスポンス(prefixes: [{prefix}], continuation_token)、エラー(401/403/500 と error: {code, message})を記載する。prefix は省略または空文字の場合にバケット直下を意味する

#### 3. ページングの扱いを明記
- 作業種別: Add
- 目的: 継続読み込みの互換性を担保するため
- 変更内容: limit は 1..1000 を受け付け、未指定時は 100 とする。continuation_token は不透明な文字列として扱い、クライアントは解析せずそのまま送信する。continuation_token が null/空の場合は次ページなしとする
