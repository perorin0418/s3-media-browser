# ChangeSet

## ChangeSet 名
- ID: changeset-01.01.01.02.02-authorization-guard-error-paths
- 所属 Task: task-01.01.01.02-s3-access-authorization-guard

## 変更対象
- 認可失敗時のフェイルクローズ処理の整備
- 未許可時に S3 一覧取得が実行されないことの担保

## ファイル一覧
※ 種別: Add / Modify / Delete

### backend/app/routes/s3.py
#### 1. 認可判定の例外をフェイルクローズとして扱う
- 作業種別: Modify
- 目的: 認可判定が不確実な場合に必ず拒否するため
- 変更内容: _internal_require_authorized_list_access で authorize_list_objects の例外を AuthorizationDeniedError に変換して送出する

#### 2. 未許可時に list_objects が呼ばれない制御を明示
- 作業種別: Modify
- 目的: 権限外ユーザーにメタデータ/オブジェクト情報が返らないようにするため
- 変更内容: list_objects_handler で認可ガードを通過した場合のみ list_objects を呼び出す

### backend/tests/test_auth_context.py
#### 1. 認可失敗時の遮断テストを追加
- 作業種別: Add
- 目的: 認可失敗時の遮断経路が明確であることを保証するため
- 変更内容: authorize_list_objects が False の場合に AuthorizationDeniedError が送出され、list_objects が呼ばれないことを検証する

#### 2. 認可判定例外のフェイルクローズテストを追加
- 作業種別: Add
- 目的: 認可判断が不確実な場合に必ず拒否されることを保証するため
- 変更内容: authorize_list_objects が例外を送出する場合に AuthorizationDeniedError が送出され、list_objects が呼ばれないことを検証する
