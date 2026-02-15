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
