# Task

## Task 名
- ID: task-1.2.1.1-bucket-folder-navigation-api
- 所属 Feature: feature-1.2.1-bucket-folder-navigation

## 作業目的
S3 のバケット一覧/プレフィックス一覧を API 経由で取得できるように、契約とバックエンド受け口を整備する。

## 作業内容
- doc/25_interfaces に一覧 API の契約を追加する
- backend のルートとゲートウェイに一覧取得の受け口を追加する
- 認証/認可のフェイルクローズを前提にする
- ページング用のトークン/件数パラメータを入出力に含める
- 変更対象(概略): doc/25_interfaces, backend/app/routes, backend/infrastructure, backend/tests

## 実装制約
- 既存の認証/認可の仕様変更は行わない
- S3 直接参照は禁止し、外部依存は関数注入で受ける
- Task にない API/スキーマ変更は行わない

## テスト観点
- 認証コンテキスト不在時はフェイルクローズされる
- 認可が false / 例外時に一覧が返らない
- ページング引数が下位関数に受け渡される

## 完了条件
- 一覧 API の契約が 25_interfaces に明記されている
- 認証/認可ガード付きの一覧ハンドラが追加されている
- 最低限の正常/異常経路がテストで確認できる

## 対象 ChangeSets
- [ ] changeset-1.2.1.1.1-define-navigation-interfaces
- [ ] changeset-1.2.1.1.2-backend-navigation-handlers

## チェックリスト
- [ ] 一覧 API 契約が追加されている
- [ ] 認証/認可ガードがフェイルクローズになっている
- [ ] ページングの入力/出力が扱える
- [ ] テストの追加範囲が明確
