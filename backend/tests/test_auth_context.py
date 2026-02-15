import pytest

from backend.app.middleware.auth_context import extract_auth_context
from backend.app.routes.s3 import AuthContextMissingError, list_objects_handler
from backend.model.auth_context import AuthContext


@pytest.mark.parametrize(
    "headers, parse_bearer_token, want_none",
    [
        ({}, lambda _: AuthContext(access_token="t", subject="s"), True),
        (
            {"Authorization": "Basic abc"},
            lambda _: AuthContext(access_token="t", subject="s"),
            True,
        ),
        (
            {"Authorization": "Bearer "},
            lambda _: AuthContext(access_token="t", subject="s"),
            True,
        ),
        (
            {"Authorization": "Bearer token"},
            lambda _: (_ for _ in ()).throw(ValueError("invalid")),
            True,
        ),
        (
            {"Authorization": "Bearer token"},
            lambda token: AuthContext(access_token=token, subject="user-1"),
            False,
        ),
    ],
)
def test_extract_auth_context(headers, parse_bearer_token, want_none):
    result = extract_auth_context(
        headers=headers,
        parse_bearer_token=parse_bearer_token,
    )

    if want_none:
        assert result is None
        return

    assert result == AuthContext(access_token="token", subject="user-1")


def test_list_objects_handler_requires_auth_context():
    with pytest.raises(AuthContextMissingError):
        list_objects_handler(
            auth_context=None,
            list_objects=lambda **_: {"ok": True},
            bucket="bucket-1",
            prefix=None,
        )


def test_list_objects_handler_passes_auth_context():
    captured = {}

    def stub_list_objects(**kwargs):
        captured.update(kwargs)
        return {"ok": True}

    auth_context = AuthContext(access_token="token", subject="user-1")

    result = list_objects_handler(
        auth_context=auth_context,
        list_objects=stub_list_objects,
        bucket="bucket-1",
        prefix="prefix-1",
    )

    assert result == {"ok": True}
    assert captured["auth_context"] == auth_context
