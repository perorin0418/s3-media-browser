from collections.abc import Callable

from backend.model.auth_context import AuthContext


class AuthContextMissingError(Exception):
    """AuthContextMissingError は認証情報が不明な場合に送出する。"""


def list_objects_handler(
    *,
    auth_context: AuthContext | None,
    list_objects: Callable[..., dict],
    bucket: str,
    prefix: str | None,
) -> dict:
    """
    list_objects_handler は S3 の一覧取得を行う。

    引数:
        auth_context: 認証コンテキスト
        list_objects: S3 一覧取得関数
        bucket: バケット名
        prefix: プレフィックス
    戻り値:
        一覧取得結果
    例外:
        AuthContextMissingError: 認証情報が不明な場合
    """
    resolved_context = _internal_require_auth_context(auth_context)
    return list_objects(
        auth_context=resolved_context,
        bucket=bucket,
        prefix=prefix,
    )


def _internal_require_auth_context(auth_context: AuthContext | None) -> AuthContext:
    if auth_context is None:
        raise AuthContextMissingError("認証情報が確認できません。")
    return auth_context
