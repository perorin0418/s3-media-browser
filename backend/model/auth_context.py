from dataclasses import dataclass


@dataclass(frozen=True)
class AuthContext:
    """
    AuthContext は認証済みの主体情報を保持する。

    引数:
        access_token: ベアラートークン
        subject: 認証主体の識別子
    """

    access_token: str
    subject: str
