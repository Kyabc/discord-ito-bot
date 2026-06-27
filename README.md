# ito Discord Bot

Discord上で遊べる会話ゲーム「ito」のBotです。

---

## Usage:
### Setup
```bash
uv sync
```

### Run the bot
```bash
uv run python main.py
```

### Run the bot with Docker
Fill the environment variables in docker-compose.yml

#### Build
```bash
docker build
```

#### Run
```bash
docker compose up
```

---

## 遊び方（itoとは）

0〜100の数字カードを各プレイヤーが1枚ずつ持ちます。

ただし、**自分の数字は直接言えません。**

代わりに「お題」に沿って例え話などで数字の大小を伝え、
全員で相談しながら小さい順に並べるゲームです。

例：
お題「行きたい旅行先」
→ 数字90の人「ハワイ」
→ 数字10の人「近所の公園」

このように感覚で伝えて並び替えます。

---

## コマンド一覧

### ゲームの準備
- `/ito create` : ゲームを作成
- `/ito join` : 参加
- `/ito leave` : 退出
- `/ito state` : 参加者確認

### ゲーム進行
- `/ito start [topic]` : ゲーム開始（お題は任意）
  - お題は自由に設定できます。お題を入力しない場合はランダムに選ばれます。
  - 参加者全員にDMで手札の番号が送信されます。
- `/ito open-cards` : カード公開

### その他
- `/ito end` : ゲーム終了
- `/ito kick @user` : プレイヤーを除外
- `/ito help` : ヘルプ表示

---

## ゲームの流れ

1. `/ito create` でゲームを作成
2. 参加者が `/ito join`
3. `/ito start` で開始
4. DMで自分の数字とお題を確認
5. 会話しながら順番を決める
6. `/ito open-cards` で答え合わせ
7. `/ito start` で次のゲームを開始、または `/ito end` でゲームを終了

---

## お題について

- あらかじめ用意されている100個のお題の中からランダムに選ばれます
- `/ito start [topic]` で直接指定も可能

**例:**
- `/ito start 行きたい旅行先`
- `/ito start 白米に合うもの`
- `/ito start 神様も引きそうなお願い`

### 補足
- 一部のお題はAIを使って生成しています。
  - 内容にばらつきがある場合がありますが、あらかじめご了承ください。
