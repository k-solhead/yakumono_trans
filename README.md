# yakumono_trans

やくもの文字変換 — Streamlit で動作するテキスト整形ツール。

Word（.docx）・Excel（.xlsx）・プレーンテキストの文字を、半角/全角の統一や約物の自動変換で整形します。
英文（en）・和文（ja）の2モードに対応。

## 機能

- **SpellCheck** — スペルチェック
- **English** — 英文テキスト整形（半角化、約物変換）
- **Japanese** — 和文テキスト整形（全角化、スラッシュ・コロン変換、数字周辺スペース除去）
- **Dictionary** — 辞書管理

### Excel セルハイライト（feature-1）

Excel ファイルを処理した際、テキスト置換によって値が変更されたセルの背景を**黄色（FFFF00）** でハイライトします。
変更の有無がひと目で分かるため、どのセルが置換対象になったかを視認できます。

- 英文（`en.py`）: `process_excel()` → `process_excel_cell()`
- 和文（`ja.py`）: `process_excel()` → `process_excel_cell_ja()`

## 使い方

```bash
cd yakumono_trans
pip install -r requirements.txt
streamlit run main.py
```

## ブランチ

| ブランチ | 説明 |
|---|---|
| `master` | ベースブランチ |
| `feature-1` | Excel セルハイライト機能追加 |

## 構成

```
yakumono_trans/
├── main.py              # エントリポイント
├── contents/
│   ├── en.py            # 英文処理
│   ├── ja.py            # 和文処理
│   ├── spell.py         # スペルチェック
│   └── dictionary.py    # 辞書ページ
├── tests/
├── output/              # 出力ディレクトリ
├── backups/
├── requirements.txt
└── Dockerfile
```
