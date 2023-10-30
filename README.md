# azure-openai-stream-trick
Azure OpenAI Service の Stream 処理をスムーズに見せかけます。すべて Azure-Samples からの引用です。

メインとなるコードは Azure-Samples のリポジトリのソースコードからの引用です。<br>
https://github.com/Azure-Samples/azure-search-openai-demo

デザインは Azure-Samples の chatgpt-quickstart を使用しています。<br>
https://github.com/Azure-Samples/chatgpt-quickstart

## 前提条件
- Python ≥ 3.10

## 使用法
1. `AZURE_OPENAI_ENDPOINT` と `AZURE_OPENAI_KEY` を環境変数にセット
1. Python 仮想環境を作成し有効化

```cmd
cd azure-openai-stream-trick
python -m venv .venv
.venv\Scripts\activate.bat
```

2. Python ライブラリをインストールして Quart サーバーを起動
```cmd
pip install -r requirements.txt
python app.py
```

## Stream と デフォルトの切り替え
`templates/index.html` の L110 のコメントを書き換えてください