import os
import random
import requests
from datetime import date
from flask import Flask, flash, redirect, render_template, request

# 📦 すでにある本物のデータファイルから情報を読み込み
from const_data import SHUGOSHIN_INFO
import messages

# 💡 手元のPC環境による「dotenvエラー」を完全に回避するセーフティ設計
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ⭕ APIキーを取得（Renderの環境変数、または手元の .env から自動取得）
API_KEY = os.environ.get("OPENAI_API_KEY", "")

# インスタンス生成
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


# --- 1. トップ画面（入力画面） ---
@app.route('/')
def index():
    return render_template('index.html')


# --- 2. 結果画面 ---
@app.route('/result', methods=['POST'])
def result():
    name = request.form.get('name', '')
    constellation = request.form.get('constellation', '') # 星座を取得
    mood = request.form.get('mood', '')                  # 気持ちを取得
    
    # 💡 エラーがあったかどうかを記録する「目印」（最初はエラーなしのFalse）
    has_error = False

    # 1. 名前の空白チェック（全角スペースも考慮）
    cleaned_name = name.strip().replace('　', '') 
    if not cleaned_name:
        flash("お名前を入力してね！", category='message')
        has_error = True  # 💡 すぐに戻らず、目印だけつける

    # 2. 星座の未選択チェック
    if not constellation:
        flash("あなたの星座を選んでね！", category='message')
        has_error = True  # 💡 目印だけつける

    # 3. 気持ちの未選択チェック
    if not mood:
        flash("今の気分を教えてね！", category='message')
        has_error = True  # 💡 目印だけつける

    # 💡 もし1つでもエラーの目印がついていたら、入力データを持ってトップに戻る
    if has_error:
        entered_data = {
            "name": name,
            "constellation": constellation,
            "mood": mood
        }
        # 引数に category='data' とつけることで、HTML側でエラー文字と区別して取得できます
        flash(entered_data, category='data')
        return redirect('/')
        
    # ➔ ーーー ここから下は、すべて正常に選ばれたときの処理 ーーー
    
    # 星座に合わせた情報を取得（エラー防止のデフォルト値も完備）
    info = SHUGOSHIN_INFO.get(constellation, {
        "name": "守護神", 
        "feature": "星たちがあなたを静かに見守っています。",
        "message": "今はゆっくり休んで、自分を大切にしてね。",
        "image": "dummy.png"
    })
    
    # 気分に合わせたメッセージをリストから選択
    if mood == 'tired':
        meigen_list = messages.tired_messages
    elif mood == 'happy':
        meigen_list = messages.happy_messages
    else:
        meigen_list = messages.default_messages

    # 今日・その気分の組み合わせでランダムに名言と運勢（★）を選択
    raw_meigen = random.choice(meigen_list)
    selected_luck = random.choice(messages.luck_list)

    # 選ばれた文章の「{name}」の部分に、実際のユーザー名を流し込む
    selected_meigen = raw_meigen.format(name=name)

    # 守護神の名前からカラー判定を行う

    shugoshin_name = info['name']

    if "ゼウス" in shugoshin_name:
        shugoshin_color = "#d97706"  # キング・ゴールド（射手座）
    elif "ヘスティア" in shugoshin_name:
        shugoshin_color = "#7c3aed"  # ロイヤル・パープル（牡牛座）
    elif "ポセイドン" in shugoshin_name:
        shugoshin_color = "#2563eb"  # オーシャン・ディープ（魚座）
    elif "アストライア" in shugoshin_name:
        shugoshin_color = "#16a34a"  # リーフ・エメラルド（乙女座）
    elif "アテナ" in shugoshin_name:
        shugoshin_color = "#1e3a8a"  # インテリ・ネイビー
    elif "アポロン" in shugoshin_name:
        shugoshin_color = "#ea580c"  # サンシャイン・オレンジ（獅子座）
    elif "アルテミス" in shugoshin_name:
        shugoshin_color = "#2dd4bf"  # ルナ・ミント（蟹座）
    elif "アレス" in shugoshin_name:
        shugoshin_color = "#dc2626"  # パッション・レッド（牡羊座）
    elif "アフロディーテ" in shugoshin_name:
        shugoshin_color = "#f43f5e"  # ラブリー・ローズ（天秤座）
    elif "ハデス" in shugoshin_name:
        shugoshin_color = "#9f1239"  # スモーキー・ガーネット（蠍座）
    elif "ヘルメス" in shugoshin_name:
        shugoshin_color = "#eab308"  # カナリア・イエロー（双子座）
    elif "クロノス" in shugoshin_name:
        shugoshin_color = "#5c537d"  # ミッドナイト・シャドウ（山羊座）
    elif "ウラヌス" in shugoshin_name:
        shugoshin_color = "#c084fc"  # マゼンタ・ワイン（水瓶座）
    else:
        shugoshin_color = "#6366f1"  # デフォルト（インディゴ）

    # 💡 『shugoshin』という1つのオブジェクト（辞書型）に荷物をまとめます
    shugoshin_data = {
        'name': shugoshin_name,
        'color': shugoshin_color,
        'image': info['image'],
        'feature': info['feature'],
        'message': info['message']
    }

    # 荷物をまとめてスッキリHTMLへリターン
    return render_template(
        'result.html',
        shugoshin=shugoshin_data,  # 名前、色、画像、メッセージが全部ここに入っています
        name=name,
        constellation=constellation,
        meigen=selected_meigen,
        luck=selected_luck
    )


# --- 3. 翻訳用の補助関数（APIルートの外に配置） ---
def translate_to_japanese(text):
    try:
        # Google翻訳の無料枠を利用するURL
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ja&dt=t&q={text}"
        response = requests.get(url, timeout=5)
        res_data = response.json()
        return "".join([sentence[0] for sentence in res_data[0] if sentence[0]])
    except Exception as e:
        print(f"翻訳エラー: {e}")
        return text


# --- 4. 神々の名言画面（外部API連携） ---
@app.route('/quote')
def quote():
    # 💡 ここを True にするとテスト用、False にすると本番用（API使用）
    test_mode = False
    
    if test_mode:
        # --- テスト用のデータ（APIを叩かない） ---
        quote_text = "【テスト表示】無限の可能性を信じれば、道は自ずと開けるでしょう。"
        author_name = "テストの守護神"
    else:
        # 🛠️ 【インデント修正完了】本番用APIの処理を正しいインデント位置へ補正しました
        url = 'https://api.thousand-api.com/v1/quotes/random'
        headers = {
            'x-api-key': API_KEY,
            'Content-Type': 'application/json'
        }
    
        try:
            # 1. APIから本物のデータを取得
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()
        
            # 2. 英語の名言と著者名を取得
            original_quote = data.get('content', 'Believe in yourself.')
            author_name = data.get('author', 'Unknown')
        
            # 3. 英語を日本語に翻訳
            quote_text = translate_to_japanese(original_quote)
            
        except Exception as e:
            print(f"APIエラー: {e}")
            quote_text = "明けない夜はないよ。僕たちはいつも君を見守っているよ。"
            author_name = "君の守護神より"

    # 4. 翻訳済みの名言を画面に送る
    return render_template('quote.html', quote=quote_text, author=author_name)


if __name__ == '__main__':
    app.run(debug=True)