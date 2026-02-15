import pytest

from backend.app.middleware.auth_context import extract_auth_context
from backend.app.routes.s3 import (
    AuthContextMissingError,
    AuthorizationDeniedError,
    list_buckets_handler,
    list_objects_handler,
    list_prefixes_handler,
)
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
            authorize_list_objects=lambda **_: True,
            bucket="bucket-1",
            prefix=None,
        )


def test_list_objects_handler_passes_auth_context():
    captured = {}

    def stub_list_objects(**kwargs):
        captured.update(kwargs)
        return {"ok": True}

    auth_context = AuthContext(access_token="token", subject="user-1")

    def stub_authorize_list_objects(**kwargs):
        captured["authorize"] = kwargs
        return True

    result = list_objects_handler(
        auth_context=auth_context,
        list_objects=stub_list_objects,
        authorize_list_objects=stub_authorize_list_objects,
        bucket="bucket-1",
        prefix="prefix-1",
    )

    assert result == {"ok": True}
    assert captured["auth_context"] == auth_context
    assert captured["authorize"]["auth_context"] == auth_context
    assert captured["authorize"]["bucket"] == "bucket-1"
    assert captured["authorize"]["prefix"] == "prefix-1"


def test_list_objects_handler_rejects_unauthorized_access():
    was_called = False

    def stub_list_objects(**_):
        nonlocal was_called
        was_called = True
        return {"ok": True}

    auth_context = AuthContext(access_token="token", subject="user-1")

    with pytest.raises(AuthorizationDeniedError):
        list_objects_handler(
            auth_context=auth_context,
            list_objects=stub_list_objects,
            authorize_list_objects=lambda **_: False,
            bucket="bucket-1",
            prefix=None,
        )

    assert was_called is False


def test_list_objects_handler_fails_close_on_authorization_exception():
    was_called = False

    def stub_list_objects(**_):
        nonlocal was_called
        was_called = True
        return {"ok": True}

    def stub_authorize_list_objects(**_):
        raise RuntimeError("boom")

    auth_context = AuthContext(access_token="token", subject="user-1")

    with pytest.raises(AuthorizationDeniedError):
        list_objects_handler(
            auth_context=auth_context,
            list_objects=stub_list_objects,
            authorize_list_objects=stub_authorize_list_objects,
            bucket="bucket-1",
            prefix=None,
        )

    assert was_called is False


def test_list_buckets_handler_requires_auth_context():
    with pytest.raises(AuthContextMissingError):
        list_buckets_handler(
            auth_context=None,
            list_buckets=lambda **_: {"ok": True},
            authorize_list_buckets=lambda **_: True,
            continuation_token=None,
            limit=None,
        )


def test_list_buckets_handler_passes_auth_context_and_paging():
    captured = {}

    def stub_list_buckets(**kwargs):
        captured["list"] = kwargs
        return {"ok": True}

    auth_context = AuthContext(access_token="token", subject="user-1")

    def stub_authorize_list_buckets(**kwargs):
        captured["authorize"] = kwargs
        return True

    result = list_buckets_handler(
        auth_context=auth_context,
        list_buckets=stub_list_buckets,
        authorize_list_buckets=stub_authorize_list_buckets,
        continuation_token="token-1",
        limit=250,
    )

    assert result == {"ok": True}
    assert captured["list"]["auth_context"] == auth_context
    assert captured["list"]["continuation_token"] == "token-1"
    assert captured["list"]["limit"] == 250
    assert captured["authorize"]["auth_context"] == auth_context


def test_list_buckets_handler_rejects_unauthorized_access():
    was_called = False

    def stub_list_buckets(**_):
        nonlocal was_called
        was_called = True
        return {"ok": True}

    auth_context = AuthContext(access_token="token", subject="user-1")

    with pytest.raises(AuthorizationDeniedError):
        list_buckets_handler(
            auth_context=auth_context,
            list_buckets=stub_list_buckets,
            authorize_list_buckets=lambda **_: False,
            continuation_token=None,
            limit=None,
        )

    assert was_called is False


def test_list_buckets_handler_fails_close_on_authorization_exception():
    was_called = False

    def stub_list_buckets(**_):
        nonlocal was_called
        was_called = True
        return {"ok": True}

    def stub_authorize_list_buckets(**_):
        raise RuntimeError("boom")

    auth_context = AuthContext(access_token="token", subject="user-1")

    with pytest.raises(AuthorizationDeniedError):
        list_buckets_handler(
            auth_context=auth_context,
            list_buckets=stub_list_buckets,
            authorize_list_buckets=stub_authorize_list_buckets,
            continuation_token=None,
            limit=None,
        )

    assert was_called is False


def test_list_prefixes_handler_requires_auth_context():
    with pytest.raises(AuthContextMissingError):
        list_prefixes_handler(
            auth_context=None,
            list_prefixes=lambda **_: {"ok": True},
            authorize_list_prefixes=lambda **_: True,
            bucket="bucket-1",
            prefix=None,
            continuation_token=None,
            limit=None,
        )


def test_list_prefixes_handler_passes_auth_context_and_paging():
    captured = {}

    def stub_list_prefixes(**kwargs):
        captured["list"] = kwargs
        return {"ok": True}

    auth_context = AuthContext(access_token="token", subject="user-1")

    def stub_authorize_list_prefixes(**kwargs):
        captured["authorize"] = kwargs
        return True

    result = list_prefixes_handler(
        auth_context=auth_context,
        list_prefixes=stub_list_prefixes,
        authorize_list_prefixes=stub_authorize_list_prefixes,
        bucket="bucket-1",
        prefix="prefix-1",
        continuation_token="token-2",
        limit=100,
    )

    assert result == {"ok": True}
    assert captured["list"]["auth_context"] == auth_context
    assert captured["list"]["bucket"] == "bucket-1"
    assert captured["list"]["prefix"] == "prefix-1"
    assert captured["list"]["continuation_token"] == "token-2"
    assert captured["list"]["limit"] == 100
    assert captured["authorize"]["auth_context"] == auth_context
    assert captured["authorize"]["bucket"] == "bucket-1"
    assert captured["authorize"]["prefix"] == "prefix-1"


def test_list_prefixes_handler_rejects_unauthorized_access():
    was_called = False

    def stub_list_prefixes(**_):
        nonlocal was_called
        was_called = True
        return {"ok": True}

    auth_context = AuthContext(access_token="token", subject="user-1")

    with pytest.raises(AuthorizationDeniedError):
        list_prefixes_handler(
            auth_context=auth_context,
            list_prefixes=stub_list_prefixes,
            authorize_list_prefixes=lambda **_: False,
            bucket="bucket-1",
            prefix=None,
            continuation_token=None,
            limit=None,
        )

    assert was_called is False


def test_list_prefixes_handler_fails_close_on_authorization_exception():
    was_called = False

    def stub_list_prefixes(**_):
        nonlocal was_called
        was_called = True
        return {"ok": True}

    def stub_authorize_list_prefixes(**_):
        raise RuntimeError("boom")

    auth_context = AuthContext(access_token="token", subject="user-1")

    with pytest.raises(AuthorizationDeniedError):
        list_prefixes_handler(
            auth_context=auth_context,
            list_prefixes=stub_list_prefixes,
            authorize_list_prefixes=stub_authorize_list_prefixes,
            bucket="bucket-1",
            prefix=None,
            continuation_token=None,
            limit=None,
        )

    assert was_called is False
