from flask import Flask, render_template, request, redirect, flash
import requests
import random
from datetime import date
import messages
# from dotenv import load_dotenv
from const_data import SHUGOSHIN_INFO
import os

# load_dotenv()
# API_KEY = os.getenv("API_KEY")

API_KEY = "hstDxwZ8x24vjqiX3WOSLGHUUGyGlff5aCRse99nsFFYh9pneVFmjrcINp37wYRe"

# インスタンス生成
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


# 結果画面
@app.route('/result', methods=['POST'])
def result():
    name = request.form.get('name', '')
    constellation = request.form.get('constellation', '') # 星座を取得
    mood = request.form.get('mood', '')                  # 気持ちを取得
    
    # 💡 エラーがあったかどうかを記録する「目印」（最初はエラーなしのFalse）
    has_error = False

    # 1. 名前の空白チェック
    cleaned_name = name.strip().replace('　', '') 
    if not cleaned_name:
        flash("お名前を入力してね！")
        has_error = True  # 💡 すぐに戻らず、目印だけつける

    # 2. 星座の未選択チェック
    if not constellation:
        flash("あなたの星座を選んでね！")
        has_error = True  # 💡 目印だけつける

    # 3. 気持ちの未選択チェック
    if not mood:
        flash("今の気分を教えてね！")
        has_error = True  # 💡 目印だけつける


    # 💡 【修正】もし1つでもエラーの目印がついていたら、入力データを持って戻る
    if has_error:
        # 入力されたデータを辞書（連想配列）にまとめます
        entered_data = {
            "name": name,
            "constellation": constellation,
            "mood": mood
        }
        # エラーメッセージとは別に、このデータも「flash」のポケットに入れます
        # （引数に category='data' とつけることで、エラー文字と区別できます）
        flash(entered_data, category='data')
        
        return redirect('/')
        
    # ➔ ーーー ここから下は、すべて正常に選ばれたときの処理 ーーー
    # （info = SHUGOSHIN_INFO.get... などの既存のコードが続きます）
    
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

    # # 🔮 【日替わりの魔法】
    # today_str = date.today().strftime("%Y%m%d")
    # random.seed(f"{today_str}_{mood}")

    # 今日・その気分の組み合わせで「絶対に固定」された名言と運勢（★）が選ばれます
    raw_meigen = random.choice(meigen_list)
    selected_luck = random.choice(messages.luck_list)

    # # 📌 ランダムのシード値をノーマル状態にリセット
    # random.seed(None)

    # 選ばれた文章の「{name}」の部分に、実際のユーザー名を流し込む
    selected_meigen = raw_meigen.format(name=name)

    # ==========================================================================
    # 🌟 【修正箇所】カラー判定の前に、守護神の名前を「info['name']」から正しく取得する
    # ==========================================================================
    shugoshin_name = info['name']

    if "ゼウス" in shugoshin_name:
        shugoshin_color = "#d97706"  # キング・ゴールド
    elif "ヘラ" in shugoshin_name:
        shugoshin_color = "#7c3aed"  # ロイヤル・パープル
    elif "ポセイドン" in shugoshin_name:
        shugoshin_color = "#2563eb"  # オーシャン・ディープ
    elif "デメテル" in shugoshin_name:
        shugoshin_color = "#16a34a"  # リーフ・エメラルド
    elif "アテナ" in shugoshin_name:
        shugoshin_color = "#1e3a8a"  # インテリ・ネイビー
    elif "アポロン" in shugoshin_name:
        shugoshin_color = "#ea580c"  # サンシャイン・オレンジ
    elif "アルテミス" in shugoshin_name:
        shugoshin_color = "#2dd4bf"  # ルナ・ミント
    elif "アレス" in shugoshin_name:
        shugoshin_color = "#dc2626"  # パッション・レッド
    elif "アフロディーテ" in shugoshin_name:
        shugoshin_color = "#f43f5e"  # ラブリー・ローズ
    elif "ヘファイストス" in shugoshin_name:
        shugoshin_color = "#9f1239"  # スモーキー・ガーネット
    elif "ヘルメス" in shugoshin_name:
        shugoshin_color = "#eab308"  # カナリア・イエロー
    elif "ディオニュソス" in shugoshin_name:
        shugoshin_color = "#c084fc"  # マゼンタ・ワイン
    else:
        shugoshin_color = "#6366f1"  # 万が一のときのデフォルト（インディゴ）

    # 💡 『shugoshin』という1つのオブジェクト（辞書型）に名前とカラーをまとめます
    shugoshin_data = {
        'name': shugoshin_name,
        'color': shugoshin_color,
        'image': info['image'],      # 💡 これらも一緒にまとめておくと、さらにFlask版らしくスッキリします！
        'feature': info['feature'],
        'message': info['message']
    }

    # ==========================================================================
    # 🌟 【これぞFlask版！】荷物がすっきりまとまった美しいリターン
    # ==========================================================================
    return render_template(
        'result.html',
        shugoshin=shugoshin_data,  # 👈 これ1つ送るだけで、名前、色、画像、メッセージが全部HTMLに届きます！
        name=name,
        constellation=constellation,
        meigen=selected_meigen,
        luck=selected_luck
    )
# 入力画面
@app.route('/')
def index():
    return render_template('index.html')

# --- 翻訳用の関数（Flaskのルートの外に置きます） ---
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

# --- 結果画面から別画面の名言へ ---
@app.route('/quote')
def quote():

    # 💡 ここを True にするとテスト用、False にすると本番用（API使用）
    test_mode = True 

    if test_mode:
        # --- テスト用のデータ（APIを叩かない） ---
        quote_text = "【テスト表示】無限の可能性を信じれば、道は自ずと開けるでしょう。"
        author_name = "テストの守護神"
    else:
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
        
        # 3. 英語を日本語に翻訳する（上の関数を呼び出し、引数にoriginal_quoteを渡す）
            quote_text = translate_to_japanese(original_quote)
            
        except Exception as e:
            print(f"APIエラー: {e}")
            quote_text = "明けない夜はないよ。僕たちはいつも君を見守っているよ。"
            author_name = "君の守護神より"

    # 4. 翻訳済みの名言を画面に送る
    return render_template('quote.html', quote=quote_text, author=author_name)

if __name__ == '__main__':
    app.run(debug=True)
    