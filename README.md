# Google Cloud Functionsでリスト形式データをスクレイピング
リスト形式のデータをスクレイピングで取得するためのソースコードです。<br>
jsonファイルで定めた特徴量を各アイテムごとに抜き出し、DataFrameに格納します。json形式でのhttpリクエストを受け取り、json形式に変換した配列を返します。
そのままCloud FunctionsにデプロイすればGASに接続しスプレッドシートへ格納することが出来ます。<br>
GASのリポジトリは[こちら](https://github.com/S-krhs/scraping_project_gas)<br>
<br>
※CloudFunctions上では`requests-html`に含まれる`arender()`が使えないようです。AWS Lambdaの場合[こちら](https://medium.com/limehome-engineering/running-pyppeteer-on-aws-lambda-with-serverless-62313b3fe3e2)の方法でpyppeteerを`/tmp`にダウンロードすることで回避できるようですが、CloudFunctionsだとそれに加えてイベントループ関連で以下のエラーが発生し動作しませんでした。
```
signal only works in main thread of the main interpreter
```
Flask関連のエラーだと思われるので、CloudRunを使用するなど自由度の高い環境で動かすことで解決できると思います。今回は動的なレンダリングが必要なサイトが無かったためこの状態でデプロイしています。<br>
レンダリングが必要になった場合はSeleniumを利用したものを改めて作成する予定です。
