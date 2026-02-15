# ChangeSet

## ChangeSet 名
- ID: changeset-01.01.01.02.01-authorization-guard-implementation
- 所属 Task: task-01.01.01.02-s3-access-authorization-guard

## 変更対象
- S3 一覧取得の認可ガード適用と責務分離
- 認可成功時のみ S3 一覧取得を許可する処理の追加

## ファイル一覧
※ 種別: Add / Modify / Delete

### backend/app/routes/s3.py
#### 1. list_objects_handler に認可判定の引数を追加
- 作業種別: Modify
- 目的: 認可成功時のみ S3 一覧取得を実行するため
- 変更内容: list_objects_handler の引数に authorize_list_objects: Callable[..., bool] を追加し、auth_context を確定した後に bucket/prefix を渡して認可する

#### 2. 認可判定を担う内部ヘルパーを追加
- 作業種別: Add
- 目的: 認可判定の責務を分離し、一覧取得処理の見通しを保つため
- 変更内容: _internal_require_authorized_list_access を追加し、authorize_list_objects が True のときのみ継続する

#### 3. 認可失敗の例外クラスを追加
- 作業種別: Add
- 目的: 認可失敗の遮断経路を明示するため
- 変更内容: AuthorizationDeniedError を追加し、認可失敗時に送出する

### backend/tests/test_auth_context.py
#### 1. 一覧取得の正常系テストを拡張
- 作業種別: Modify
- 目的: 認可ガード導入後の正常系を保証するため
- 変更内容: test_list_objects_handler_passes_auth_context で authorize_list_objects が True のとき list_objects が呼ばれることを検証する
