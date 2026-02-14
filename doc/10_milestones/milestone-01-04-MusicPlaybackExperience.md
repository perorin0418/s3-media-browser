# Milestone

## Milestone 名
- ID: milestone-01-04-MusicPlaybackExperience
- 対応 Vision: vision-01-s3-media-browser

## 目的
音楽フォルダの連続再生・シャッフル再生を 1 操作で開始できる体験を提供する。

## スコープ
### 含む
- フォルダ単位のプレイリスト生成
- 連続再生/シャッフル再生の開始
- 再生操作（再生/停止/次へ/前へ）
- 再生状態の保持（セッション内）

### 含まない
- 音源の編集/加工/変換
- 高度なプレイリスト編集（並び替えや共有）
- バックグラウンド常時再生の保証

## 完了条件（Definition of Done）
- 1 操作でフォルダの連続再生またはシャッフル再生を開始できる
- 再生中の離脱率が 20% 未満となる体験を狙える
- 再生中に権限が失効した場合はアクセスが停止される
- 再生 UI が現在の曲と操作状態を明確に示す
- セッション内で再生状態が維持される

## 対象 Feature
- [ ] feature-01.04.01-music-folder-playback
- [ ] feature-01.04.02-shuffle-and-queue
- [ ] feature-01.04.03-player-controls-ui
- [ ] feature-01.04.04-playback-state-session

## 依存関係
- 前提条件: milestone-01-01-SecureBrowseFoundation の認証・認可/閲覧基盤
- 後続への影響: 音楽利用ログや共有再生の検討余地が生まれる

## リスク・注意点
- ブラウザの自動再生制限により開始操作が制約される
- 大量曲数の読み込みによる初期遅延
- 注意: 詳細仕様は Feature / Task で定義する
