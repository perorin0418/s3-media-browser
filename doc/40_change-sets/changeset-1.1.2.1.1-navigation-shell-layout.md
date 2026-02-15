# ChangeSet

## ChangeSet 名
- ID: changeset-1.1.2.1.1-navigation-shell-layout
- 所属 Task: task-1.1-2.1-secure-navigation-shell

## 変更対象
- frontend/app.vue

## ファイル一覧
※ 種別: Add / Modify / Delete

### frontend/app.vue
#### 1. 認証済みユーザー向けナビゲーションシェルの骨格を追加
- 作業種別: Modify
- 目的: 認証済みユーザーのみが到達できる共通シェルを提供するため
- 変更内容: `NuxtPage` をヘッダー/ナビゲーション/メイン枠で囲むレイアウトを追加し、主要導線（ホーム/閲覧入口/サインアウト）を配置する。ホーム/閲覧入口は既存の閲覧入口ページ（frontend/pages/index.vue）へのリンクとして同一の遷移先を使用し、サインアウトは `useAuth.buildHostedUiSignOutUrl()` で取得した URL へ遷移するリンク/ボタンを配置する

#### 2. 認証状態未確定時の描画抑止を追加
- 作業種別: Modify
- 目的: 認証状態が不確定な間に閲覧 UI を描画しないため
- 変更内容: `useAuth` の `status` を参照し、`authenticated` の場合のみナビゲーションシェルと `NuxtPage` を描画する