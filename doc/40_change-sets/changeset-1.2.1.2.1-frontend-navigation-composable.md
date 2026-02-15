# ChangeSet

## ChangeSet 名
- ID: changeset-1.2.1.2.1-frontend-navigation-composable
- 所属 Task: task-1.2.1.2-bucket-folder-navigation-ui

## 変更対象
- frontend/nuxt.config.ts
- frontend/types/s3Navigation.ts
- frontend/composables/useS3Navigation.ts

## ファイル一覧
※ 種別: Add / Modify / Delete

### frontend/nuxt.config.ts
#### 1. API ベース URL を追加
- 作業種別: Modify
- 目的: 環境ごとの API 切替を可能にするため
- 変更内容: runtimeConfig.public.apiBaseUrl を追加し、空文字の場合は相対パスとして扱う前提を記載する

### frontend/types/s3Navigation.ts
#### 1. 一覧 API の型定義を追加
- 作業種別: Add
- 目的: バケット/プレフィックス一覧の入出力を型で固定するため
- 変更内容: BucketItem/PrefixItem/ListBucketsResponse/ListPrefixesResponse などの型を追加する

### frontend/composables/useS3Navigation.ts
#### 1. 一覧 API 呼び出し composable を追加
- 作業種別: Add
- 目的: pages/ の API 直接呼び出しを避け、責務を集約するため
- 変更内容: useAuth の accessToken を利用し、listBuckets/listPrefixes を提供する
