# ChangeSet

## ChangeSet 名
- ID: changeset-01.01.01.01.03-api-auth-context-wiring
- 所属 Task: task-01.01.01.01-auth-flow-baseline

## 目的
API 層で認証コンテキストを受け取り、S3 関連 API 呼び出しに引き渡す受け口を用意する。

## 受け入れ基準
- API リクエストから認証コンテキストを抽出できる
- S3 関連 API のハンドラが認証コンテキストを受け取る
- 認証状態が不確実な場合はフェイルクローズで拒否する
- 具体的な認可ロジックは追加しない
- 認証コンテキストは `@dataclass(frozen=True)` で定義される
- 外部依存は関数引数で注入され、パッチ系モックに依存しない

## 変更対象
- backend/ の S3 関連 API 呼び出しに認証コンテキストを受け渡す層

## 対象ファイル
- backend/app/middleware/auth_context.py
- backend/app/routes/s3.py
- backend/infrastructure/s3_gateway.py
- backend/model/auth_context.py
- backend/tests/test_auth_context.py

## 作業計画
1. 認証コンテキストの型定義を追加する
2. リクエストから認証コンテキストを抽出するミドルウェアを追加する
3. S3 関連ルートで認証コンテキストの必須化と受け渡しを行う
4. 認証不確実時のフェイルクローズ判定を追加する
5. 認証コンテキスト抽出の最小テストをパラメタライズで追加する

## ファイル一覧
※ 種別: Add / Modify / Delete

### backend/model/auth_context.py
#### 1. 認証コンテキスト型を追加
- 作業種別: Add
- 目的: 認証情報の受け渡しを明示するため
- 変更内容: `@dataclass(frozen=True)` でトークンと主体情報を保持する構造体を追加

### backend/app/middleware/auth_context.py
#### 1. 認証コンテキスト抽出処理を追加
- 作業種別: Add
- 目的: API で認証状態を一元的に扱うため
- 変更内容: リクエストヘッダーからの抽出と失敗時の判定を追加（依存は引数注入）

### backend/app/routes/s3.py
#### 1. 認証コンテキストを受け取るハンドラに変更
- 作業種別: Modify
- 目的: S3 API 呼び出しに認証コンテキストを付与するため
- 変更内容: ハンドラの入力に認証コンテキストを追加（外部依存は引数注入）

#### 2. 認証不確実時の遮断処理を追加
- 作業種別: Modify
- 目的: フェイルクローズを徹底するため
- 変更内容: 認証コンテキスト不在時の拒否処理を追加

### backend/infrastructure/s3_gateway.py
#### 1. 認証コンテキストの受け渡し口を追加
- 作業種別: Modify
- 目的: 後続の認可ロジック接続点を用意するため
- 変更内容: S3 呼び出し関数に認証コンテキスト引数を追加

### backend/tests/test_auth_context.py
#### 1. 認証コンテキスト抽出テストを追加
- 作業種別: Add
- 目的: 認証不確実時のフェイルクローズを確認するため
- 変更内容: ヘッダー欠損/不正時の拒否ケースをパラメタライズで追加
