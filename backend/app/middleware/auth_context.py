from collections.abc import Callable, Mapping

from backend.model.auth_context import AuthContext


def extract_auth_context(
    *,
    headers: Mapping[str, str],
    parse_bearer_token: Callable[[str], AuthContext],
) -> AuthContext | None:
    """
    extract_auth_context はリクエストヘッダーから認証コンテキストを抽出する。

    引数:
        headers: リクエストヘッダー
        parse_bearer_token: ベアラートークンから AuthContext を生成する関数
    戻り値:
        抽出できた場合は AuthContext、それ以外は None
    """
    auth_header = _internal_find_header_value(headers, "authorization")
    if not auth_header:
        return None

    access_token = _internal_parse_bearer_header(auth_header)
    if not access_token:
        return None

    try:
        return parse_bearer_token(access_token)
    except (ValueError, TypeError):
        return None


def _internal_find_header_value(headers: Mapping[str, str], key: str) -> str | None:
    target = key.lower()
    for header_key, value in headers.items():
        if header_key.lower() == target:
            return value
    return None


def _internal_parse_bearer_header(auth_header: str) -> str | None:
    normalized = auth_header.strip()
    if not normalized.lower().startswith("bearer "):
        return None

    token = normalized[7:].strip()
    if not token:
        return None

    return token
