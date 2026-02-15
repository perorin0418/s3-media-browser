from collections.abc import Callable

from backend.model.auth_context import AuthContext


def list_objects(
    *,
    auth_context: AuthContext,
    fetch_list_objects: Callable[..., dict],
    bucket: str,
    prefix: str | None,
) -> dict:
    """
    list_objects は S3 の一覧取得を委譲する。

    引数:
        auth_context: 認証コンテキスト
        fetch_list_objects: 実際の S3 呼び出し関数
        bucket: バケット名
        prefix: プレフィックス
    戻り値:
        一覧取得結果
    """
    return fetch_list_objects(
        auth_context=auth_context,
        bucket=bucket,
        prefix=prefix,
    )


def list_buckets(
    *,
    auth_context: AuthContext,
    fetch_list_buckets: Callable[..., dict],
    continuation_token: str | None,
    limit: int | None,
) -> dict:
    """
    list_buckets は S3 のバケット一覧取得を委譲する。

    引数:
        auth_context: 認証コンテキスト
        fetch_list_buckets: 実際の S3 呼び出し関数
        continuation_token: 継続トークン
        limit: 取得件数
    戻り値:
        一覧取得結果
    """
    return fetch_list_buckets(
        auth_context=auth_context,
        continuation_token=continuation_token,
        limit=limit,
    )


def list_prefixes(
    *,
    auth_context: AuthContext,
    fetch_list_prefixes: Callable[..., dict],
    bucket: str,
    prefix: str | None,
    continuation_token: str | None,
    limit: int | None,
) -> dict:
    """
    list_prefixes は S3 のプレフィックス一覧取得を委譲する。

    引数:
        auth_context: 認証コンテキスト
        fetch_list_prefixes: 実際の S3 呼び出し関数
        bucket: バケット名
        prefix: プレフィックス
        continuation_token: 継続トークン
        limit: 取得件数
    戻り値:
        一覧取得結果
    """
    return fetch_list_prefixes(
        auth_context=auth_context,
        bucket=bucket,
        prefix=prefix,
        continuation_token=continuation_token,
        limit=limit,
    )
