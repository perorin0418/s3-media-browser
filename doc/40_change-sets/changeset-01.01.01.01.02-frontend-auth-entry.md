# ChangeSet

## ChangeSet 名
- ID: changeset-01.01.01.01.02-frontend-auth-entry
- 所属 Task: task-01.01.01.01-auth-flow-baseline

## 目的
Hosted UI を利用したサインイン導線とコールバック処理を追加し、未認証アクセスを遮断する入口を整える。

## 受け入れ基準
- サインイン入口が Hosted UI に遷移する
- コールバックで認証状態を取得し、セッションを保持できる
- 未認証または認証不確実時に閲覧入口が遮断される
- 認証状態の判定はフェイルクローズである

## 変更対象
- frontend/ の認証入口（サインイン/コールバック）と認証状態参照の UI モジュール

## 対象ファイル
- frontend/pages/signin.vue
- frontend/pages/auth/callback.vue
- frontend/composables/useAuth.ts
- frontend/middleware/requireAuth.ts
- frontend/pages/index.vue

## 作業計画
1. サインインページを追加し、Hosted UI への遷移処理を実装する
2. コールバックページを追加し、認証コード/トークンの取得処理を実装する
3. 認証状態の保持と参照を `useAuth` に集約する
4. 認証必須のページに `requireAuth` を適用し、未認証を遮断する
5. 認証状態が不確実な場合はフェイルクローズで扱う

## ファイル一覧
※ 種別: Add / Modify / Delete

### frontend/pages/signin.vue
#### 1. Hosted UI への遷移ボタンを追加
- 作業種別: Add
- 目的: サインイン導線を確立するため
- 変更内容: Hosted UI の URL へリダイレクトする UI と処理を追加

### frontend/pages/auth/callback.vue
#### 1. コールバック処理を追加
- 作業種別: Add
- 目的: 認証状態を取得して保持するため
- 変更内容: 認証コード/トークンの受け口と保存処理を追加

### frontend/composables/useAuth.ts
#### 1. 認証状態の管理ロジックを追加
- 作業種別: Add
- 目的: 認証状態の参照口を一元化するため
- 変更内容: 認証状態取得、保存、破棄の関数を追加

### frontend/middleware/requireAuth.ts
#### 1. 未認証時のアクセス遮断を追加
- 作業種別: Add
- 目的: 閲覧入口を保護するため
- 変更内容: 認証不確実時を含むフェイルクローズ判定を追加

### frontend/pages/index.vue
#### 1. 認証ガードを適用
- 作業種別: Modify
- 目的: 未認証ユーザーの閲覧入口アクセスを遮断するため
- 変更内容: `requireAuth` ミドルウェアを適用
