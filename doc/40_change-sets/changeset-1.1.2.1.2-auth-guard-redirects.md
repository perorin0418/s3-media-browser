# ChangeSet

## ChangeSet 名
- ID: changeset-1.1.2.1.2-auth-guard-redirects
- 所属 Task: task-1.1-2.1-secure-navigation-shell

## 変更対象
- frontend/middleware/requireAuth.ts
- frontend/composables/useAuth.ts

## ファイル一覧
※ 種別: Add / Modify / Delete

### frontend/middleware/requireAuth.ts
#### 1. 認証状態の解決結果を使用する
- 作業種別: Modify
- 目的: 初期表示と画面遷移時に認証状態を検証するため
- 変更内容: ミドルウェア開始時に `useAuth.resolveAuthStatus()` を呼び出し、戻り値の `status` に基づいて認証判定を行う（`unknown` を含む `authenticated` 以外は未認証扱い）

#### 2. 未認証時の既存認証入口への遷移を統一
- 作業種別: Modify
- 目的: 未認証/期限切れ/検証失敗/更新失敗のいずれもサインイン導線へ戻すため
- 変更内容: `status` が `authenticated` 以外、または `isAuthenticatedWithFreshToken()` が false の場合は、既存のサインインページ（frontend/pages/signin.vue）へ遷移する

### frontend/composables/useAuth.ts
#### 1. 認証状態の解決ヘルパーを追加
- 作業種別: Modify
- 目的: 初期表示/画面遷移時に認証状態を確定させるため
- 変更内容: `resolveAuthStatus()` を追加し、クライアントかつ `status` が `unknown` の場合に `loadFromStorage()` を実行してから `status` を返す。`loadFromStorage()` の結果が無効/期限切れの場合は `unauthenticated` が返る