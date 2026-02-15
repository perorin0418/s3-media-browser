# AWS CDK インフラ構成管理（Python）

この `infra` ディレクトリは、AWS Cloud Development Kit (CDK, Python) を用いたインフラ構成管理用プロジェクトです。

## 前提環境
- Python 3.12 以上
- [uv](https://github.com/astral-sh/uv) インストール済み（依存パッケージ管理用）
- AWS CLI認証済み（`aws configure`コマンド等で事前に設定を行ってください）

## セットアップ手順

1. **仮想環境の有効化**

   Windows:
   ```sh
   .venv\Scripts\activate.ps1
   ```
   Unix/Mac:
   ```sh
   source .venv/bin/activate
   ```

1. **依存パッケージのインストール**

   プロジェクトディレクトリで下記を実行してください：

   ```sh
   uv sync
   ```

## CDK 利用例

- **CDKアプリの合成（CloudFormationテンプレート生成）**

  ```sh
  cdk synth --profile private
  ```

- **CDK環境の初期化**

  ```sh
  cdk bootstrap --profile private aws://698807804820/ap-northeast-1
  cdk bootstrap --profile private aws://698807804820/us-east-1
  ```

- **環境差分確認**

  ```sh
  cdk diff --profile private
  ```

- **デプロイ（リソース作成/更新）**

  ```sh
  cdk deploy --profile private --all
  ```

- **リソース削除（スタック破棄）**

  ```sh
  cdk destroy --profile private
  ```

## Tips・トラブルシューティング
- Pythonパスやモジュールimportエラー時は `__init__.py` の有無や、パス指定に注意してください。
- AWS認証の未設定時は `aws configure` でaccess/secret key等を準備してください。
- 依存パッケージ追加・更新後は `uv pip install -e .` を再実行推奨。
- deprecated警告が出る場合は、公式ドキュメント等を参照し新しいAPIへの移行を検討してください。

## 参考リンク
- [AWS CDK Python 公式ドキュメント](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html)
- [uv 公式リポジトリ](https://github.com/astral-sh/uv)
