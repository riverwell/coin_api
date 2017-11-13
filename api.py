#!/usr/bin/env python
# coding: utf-8


import subprocess
from flask import Flask, jsonify, request

# ノードを作る
app = Flask(__name__)


# メソッドはPOSTで/transfer エンドポイントを作る。メソッドはPOSTなのでデータを送信する
@app.route('/transfer', methods=['POST'])
def transfer():
    values = request.get_json()

    # POSTされたデータに必要なデータがあるか確認
    required = ['sender', 'receiver', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    subprocess.call(
        'curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0","id":76981351,"method":"personal_unlockAccount","params":["0x57b9469ec757d0ac4aeee0b532c1ae9bd7a38301","next123"]}\' http://localhost:8575',
        shell=True)

    subprocess.call(
        'curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0","id":29141882,"method":"eth_sendTransaction","params":[{"from":"0x57b9469ec757d0ac4aeee0b532c1ae9bd7a38301","to":"0x09a68b226e01e37bc67c8a1a1a2d877a2b3e27c1","value":"0xde0b6b3a7640000"}]}\' http://localhost:8575',
        shell=True)

    response = {'message': f'送信されました'}
    return jsonify(response), 201


# メソッドはPOSTで、ウォレットをリターンする/get_balanceエンドポイントを作る
@app.route('/get_balance', methods=['POST'])
def get_balance():
    values = request.get_json()

    # POSTされたデータに必要なデータがあるか確認
    required = ['account']
    if not all(k in values for k in required):
        return 'Missing values', 400

    result = popen(
        'curl -X POST -H "Content-Type: application/json" -d \'{"jsonrpc":"2.0","method":"eth_getBalance","params":["0x57b9469ec757d0ac4aeee0b532c1ae9bd7a38301", "latest"],"id":1}\' http://localhost:8575')

    # todo 1/10^18にする
    response = {'message': f'{result}'}
    return jsonify(response), 201


def popen(cmd):
    """シェルの実行結果を取得する"""
    outputs = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = outputs.communicate()
    # bytesで受け取った結果をstrに変換する
    return [s for s in stdout.decode('utf-8').split('\n') if s]


def main():
    # port5000でサーバーを起動する
    app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
