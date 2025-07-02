from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import random

# FlaskアプリとSocketIOを初期化
app = Flask(__name__)
socketio = SocketIO(app)

# サーバーがダミーデータを生成し続ける関数
def generate_dummy_data():
    """2秒ごとに新しいダミーデータを生成してブラウザに送信する"""
    print("ダミーデータの送信を開始します...")
    while True:
        dummy_data = {
            'temp': round(25 + random.uniform(-1.5, 1.5), 2),
            'hum': round(50 + random.uniform(-5, 5), 2),
            'pres': round(1013 + random.uniform(-2, 2), 2),
            'gas': round(50000 + random.uniform(-10000, 10000), 2)
        }
        # 'update_data'というイベント名で、データをクライアント(ブラウザ)に送信
        socketio.emit('update_data', dummy_data)
        socketio.sleep(2) # 2秒待機

# 誰かがWebページに初めて接続したときに呼ばれる処理
@socketio.on('connect')
def on_connect():
    print('クライアントが接続しました！')
    # 新しい接続があるたびに、バックグラウンドでデータ生成タスクを開始
    socketio.start_background_task(generate_dummy_data)

# WebページのルートURL（例: http://.../）にアクセスしたときに呼ばれる処理
@app.route('/')
def index():
    # templatesフォルダの中のindex.htmlファイルを表示する
    return render_template('index.html')

# このファイルが直接実行された場合にサーバーを起動
if __name__ == '__main__':
    socketio.run(app)