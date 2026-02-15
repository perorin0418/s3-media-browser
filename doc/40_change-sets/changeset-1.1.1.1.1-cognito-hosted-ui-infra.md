# ChangeSet

## ChangeSet 名
- ID: changeset-1.1.1.1.1-cognito-hosted-ui-infra
- 所属 Task: task-1.1.1.1-auth-flow-baseline

## 目的
CDK（Python）で Cognito User Pool と Hosted UI を構成し、フロントエンドが参照する認証導線の基盤を確定する。

## 受け入れ基準
- Cognito User Pool、App Client、Hosted UI ドメインが CDK 定義として追加されている
- コールバック URL とログアウト URL が設定として明示されている
- フロントエンドが参照する Hosted UI のドメインと Client ID が安定した経路で参照できる
- 既存の権限モデルを変更しない

## 変更対象
- infra/ の Cognito および Hosted UI 設定を管理する CDK スタック

## 対象ファイル
- infra/app.py
- infra/cdk_constructs/auth_construct.py
- infra/cdk_stacks/auth_stack.py
- infra/cdk_config/auth_settings.py
- infra/cdk_tests/test_auth_stack.py

## 作業計画
1. CDK アプリのエントリを追加し、認証スタックを読み込む
2. Cognito/Hosted UI を定義する Construct を追加する
3. AuthStack は Construct を組み立てるだけの構成にする
4. Hosted UI ドメインとコールバック/ログアウト URL を設定として分離する
5. フロントエンド参照用に、安定 ID 経由（例: SSM Parameter）で設定値を公開する
6. CDK のスタック検証テストを追加する

## ファイル一覧
※ 種別: Add / Modify / Delete

### infra/app.py
#### 1. 認証スタックを起動するエントリを追加
- 作業種別: Add
- 目的: CDK アプリとして Cognito 構成をデプロイ可能にするため
- 変更内容: `AuthStack` の生成と環境設定を追加

### infra/cdk_constructs/auth_construct.py
#### 1. Cognito/Hosted UI の Construct を追加
- 作業種別: Add
- 目的: Stack を肥大化させず再利用可能な構成にするため
- 変更内容: User Pool、App Client、Hosted UI、SSM Parameter をまとめて定義

### infra/cdk_stacks/auth_stack.py
#### 1. AuthConstruct を組み立てる
- 作業種別: Modify
- 目的: Stack は Construct の組み立てに専念させるため
- 変更内容: AuthConstruct を生成し設定を渡す

### infra/cdk_config/auth_settings.py
#### 1. Hosted UI の URL 設定を定義
- 作業種別: Add
- 目的: コールバック/ログアウト URL を明示し再利用可能にするため
- 変更内容: URL リストと環境差分の設定を追加

### infra/cdk_tests/test_auth_stack.py
#### 1. Cognito/Hosted UI の構成を検証
- 作業種別: Add
- 目的: CDK 定義が期待通りに出力されることを確認するため
- 変更内容: User Pool、App Client、ドメイン、参照経路の存在確認テストを追加
