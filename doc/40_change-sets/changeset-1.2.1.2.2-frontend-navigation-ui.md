# ChangeSet

## ChangeSet 名
- ID: changeset-1.2.1.2.2-frontend-navigation-ui
- 所属 Task: task-1.2.1.2-bucket-folder-navigation-ui

## 変更対象
- frontend/pages/index.vue

## ファイル一覧
※ 種別: Add / Modify / Delete

### frontend/pages/index.vue
#### 1. 一覧ナビゲーション UI を追加
- 作業種別: Modify
- 目的: バケット/プレフィックスを UI で辿れるようにするため
- 変更内容: ルートではバケット一覧を表示し、バケット/プレフィックスのクリックで階層移動、パンくずクリックで任意階層へ戻る。戻り操作は 1 階層戻りとして提供し、階層ごとに一覧/continuation_token を分離して管理する(階層遷移時はトークンをリセット)。一覧取得は useS3Navigation 経由で行う

#### 2. ページングとエラーハンドリングを追加
- 作業種別: Modify
- 目的: 大量オブジェクトに備え、失敗時に再試行できるようにするため
- 変更内容: continuation_token がある場合のみ継続読み込みボタンを表示し、継続読み込みは既存一覧へ追記する。API 失敗時はエラーメッセージと再試行ボタンを表示する
