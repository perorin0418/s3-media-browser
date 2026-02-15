# Task

## Task 名
- ID: task-1.2.1.2-bucket-folder-navigation-ui
- 所属 Feature: feature-1.2.1-bucket-folder-navigation

## 作業目的
バケット/フォルダ階層を UI 上で安全に辿れる一覧ナビゲーションを提供する。

## 作業内容
- 一覧 API 呼び出しを composable に集約する
- パンくずと戻り操作を備えた一覧 UI を整備する
- ページング(継続読み込み)を UI で扱えるようにする
- エラー時は明確なメッセージと再試行導線を表示する
- 変更対象(概略): frontend/composables, frontend/pages, frontend/types, frontend/nuxt.config.ts

## 実装制約
- pages/ からの直接 API 呼び出しは禁止
- 認証トークンは useAuth から取得する
- 既存の認証導線/Hosted UI は変更しない
- Task にない UI/導線追加は行わない

## テスト観点
- ルート階層でバケット一覧が表示される
- バケット選択でプレフィックス一覧に遷移する
- パンくずが現在位置を示す
- ページングの継続読み込みができる
- API エラー時に再試行できる

## 完了条件
- バケット/フォルダを一覧操作で移動できる
- パンくずで現在位置が明確に把握できる
- ページングが UI から利用できる
- 未認証/未認可は既存ガードで遮断される

## 対象 ChangeSets
- [ ] changeset-1.2.1.2.1-frontend-navigation-composable
- [ ] changeset-1.2.1.2.2-frontend-navigation-ui

## チェックリスト
- [ ] pages/ に直接 API 呼び出しがない
- [ ] useAuth トークンが利用されている
- [ ] パンくず/戻り操作が提供されている
- [ ] ページングが UI から操作できる
- [ ] エラー時に再試行導線がある
