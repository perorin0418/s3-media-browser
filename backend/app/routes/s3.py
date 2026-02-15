from collections.abc import Callable

from backend.model.auth_context import AuthContext


class AuthContextMissingError(Exception):
    """AuthContextMissingError は認証情報が不明な場合に送出する。"""


class AuthorizationDeniedError(Exception):
    """AuthorizationDeniedError は認可失敗時に送出する。"""


def list_objects_handler(
    *,
    auth_context: AuthContext | None,
    list_objects: Callable[..., dict],
    authorize_list_objects: Callable[..., bool],
    bucket: str,
    prefix: str | None,
) -> dict:
    """
    list_objects_handler は S3 の一覧取得を行う。

    引数:
        auth_context: 認証コンテキスト
        list_objects: S3 一覧取得関数
        authorize_list_objects: 一覧取得の認可判定関数
        bucket: バケット名
        prefix: プレフィックス
    戻り値:
        一覧取得結果
    例外:
        AuthContextMissingError: 認証情報が不明な場合
        AuthorizationDeniedError: 認可に失敗した場合
    """
    resolved_context = _internal_require_auth_context(auth_context)
    _internal_require_authorized_access(
        authorize=authorize_list_objects,
        auth_context=resolved_context,
        bucket=bucket,
        prefix=prefix,
    )
    return list_objects(
        auth_context=resolved_context,
        bucket=bucket,
        prefix=prefix,
    )


def list_buckets_handler(
    *,
    auth_context: AuthContext | None,
    list_buckets: Callable[..., dict],
    authorize_list_buckets: Callable[..., bool],
    continuation_token: str | None,
    limit: int | None,
) -> dict:
    """
    list_buckets_handler は S3 のバケット一覧取得を行う。

    引数:
        auth_context: 認証コンテキスト
        list_buckets: バケット一覧取得関数
        authorize_list_buckets: バケット一覧の認可判定関数
        continuation_token: 継続トークン
        limit: 取得件数
    戻り値:
        一覧取得結果
    例外:
        AuthContextMissingError: 認証情報が不明な場合
        AuthorizationDeniedError: 認可に失敗した場合
    """
    resolved_context = _internal_require_auth_context(auth_context)
    _internal_require_authorized_access(
        authorize=authorize_list_buckets,
        auth_context=resolved_context,
    )
    return list_buckets(
        auth_context=resolved_context,
        continuation_token=continuation_token,
        limit=limit,
    )


def list_prefixes_handler(
    *,
    auth_context: AuthContext | None,
    list_prefixes: Callable[..., dict],
    authorize_list_prefixes: Callable[..., bool],
    bucket: str,
    prefix: str | None,
    continuation_token: str | None,
    limit: int | None,
) -> dict:
    """
    list_prefixes_handler は S3 のプレフィックス一覧取得を行う。

    引数:
        auth_context: 認証コンテキスト
        list_prefixes: プレフィックス一覧取得関数
        authorize_list_prefixes: プレフィックス一覧の認可判定関数
        bucket: バケット名
        prefix: プレフィックス
        continuation_token: 継続トークン
        limit: 取得件数
    戻り値:
        一覧取得結果
    例外:
        AuthContextMissingError: 認証情報が不明な場合
        AuthorizationDeniedError: 認可に失敗した場合
    """
    resolved_context = _internal_require_auth_context(auth_context)
    _internal_require_authorized_access(
        authorize=authorize_list_prefixes,
        auth_context=resolved_context,
        bucket=bucket,
        prefix=prefix,
    )
    return list_prefixes(
        auth_context=resolved_context,
        bucket=bucket,
        prefix=prefix,
        continuation_token=continuation_token,
        limit=limit,
    )


def _internal_require_auth_context(auth_context: AuthContext | None) -> AuthContext:
    if auth_context is None:
        raise AuthContextMissingError("認証情報が確認できません。")
    return auth_context


def _internal_require_authorized_access(
    *,
    authorize: Callable[..., bool],
    **kwargs: object,
) -> None:
    try:
        allowed = authorize(**kwargs)
    except Exception as exc:
        raise AuthorizationDeniedError("一覧取得の認可に失敗しました。") from exc
    if not allowed:
        raise AuthorizationDeniedError("一覧取得の認可に失敗しました。")
