# Oracle Docs スクレイパー

Oracle Cloud Infrastructure (OCI) のドキュメントをオフラインでアクセスできるようにダウンロードするための Python ベースの Web スクレイパーです。このツールは OCI ドキュメントを再帰的にスクレイピングし、元のディレクトリ構造を維持します。

## 主な機能

- OCI ドキュメントページの再帰的スクレイピング
- 保存したファイルの元のドキュメント構造の維持
- サーバーに負荷をかけない適切な間隔でのスクレイピング
- 包括的なログ記録
- OCI ドキュメントドメイン内での URL 検証
- 相対 URL と絶対 URL の処理

## 必要条件

- Python 3.x
- 依存パッケージ:
  - requests==2.31.0
  - beautifulsoup4==4.12.2
  - urllib3==2.0.7

## インストール方法

1. リポジトリのクローン:
```bash
git clone [your-repository-url]
cd docs-scraper
```

2. 必要なパッケージのインストール:
```bash
pip install -r requirements.txt
```

3. (オプション) Docker でのビルドと実行:
```bash
docker build -t oracle-docs-scraper .
docker run oracle-docs-scraper
```

## 使用方法

1. スクレイパーの実行:
```bash
python oracle_docs_scraper.py
```

スクレイパーは以下の動作を行います:
- 日本語版 OCI ドキュメントのホームページから開始
- HTML コンテンツを `htmls` ディレクトリにダウンロード
- 保存ファイルで元の URL 構造を維持
- 進行状況とエラーのログを記録

## 設定

メインスクリプト (`oracle_docs_scraper.py`) には以下の設定可能なパラメータがあります:

- `base_url`: スクレイピングを開始する URL (デフォルト: 日本語版 OCI ドキュメント)
- `output_dir`: スクレイピングしたファイルを保存するディレクトリ (デフォルト: "htmls")

## 機能の詳細

### URL 検証
- docs.oracle.com ドメイン内の URL であることを確認
- ドキュメント以外の URL をフィルタリング
- バイナリファイル（PDF、ZIP、画像）を除外

### ファイル整理
- URL 構造に合わせたディレクトリの作成
- 不要なパスコンポーネント（"iaas"、"Content"）の削除
- 必要に応じてファイルに .html 拡張子を追加

### エラー処理
- 包括的なログシステム
- ネットワークエラーの適切な処理
- 既に訪問済みの URL のスキップ

### レート制限
- サーバーに負荷をかけないよう1秒間の遅延を設定
