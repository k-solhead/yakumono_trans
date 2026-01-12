import streamlit as st
from spellchecker import SpellChecker # Using pyspellchecker instead
import json
import shutil
import os
from datetime import datetime

local_dic = "my_custom_dict.json"
backup_dir = "backups"
spell = SpellChecker(local_dictionary=local_dic)

st.title("スペルチェック辞書管理用ページ")
st.error("管理用のページです。さわらないでください‼")

add_word = st.text_input("辞書に登録したいスペルを入力")
if st.button("登録"):
    spell.word_frequency.add(add_word)
    # カスタム辞書データをエクスポート
    spell.export(local_dic, gzipped=False)

del_word = st.text_input("辞書から削除したいスペルを入力")
if st.button("削除"):
    spell.word_frequency.remove(del_word) 
    # カスタム辞書データをエクスポート
    spell.export(local_dic, gzipped=False)

st.subheader("辞書のダウンロード")
# データをJSON形式の文字列に変換し、バイト列としてエンコード
f = open(local_dic, 'r')
json_dict = json.load(f)
json_str = json.dumps(json_dict)

st.download_button(
    label="辞書をダウンロード",
    data=json_str,
    file_name='my_custom_dict.json',
    mime='application/json',
)

with st.expander("辞書上書き"):
    uploaded_file = st.file_uploader("上書きする辞書ファイルをアップロードしてください", type="json")
    
    if uploaded_file is not None:
        try:
            data = json.loads(uploaded_file)
            
            st.success("JSONファイルが正常に読み込まれました")
            
            # バックアップディレクトリが存在しない場合は作成
            os.makedirs(backup_dir, exist_ok=True)
            
            # 2. バックアップファイルの作成 (コピー)
            timestamp = datetime.now().strftime('%Y%MMDD') # YYYYMMDD形式の日付
            backup_file_name = f"{os.path.splitext(local_dic)[0]}-backup{timestamp}{os.path.splitext(local_dic)[1]}"
            backup_path = os.path.join(backup_dir, backup_file_name)

            # 元ファイルの更新日時も保持してコピー
            shutil.copy2(local_dic, backup_path)
            print(f"バックアップを作成しました: {backup_path}")
            
            # 元ファイルを上書き保存
            with open(local_dic, 'w', encoding='utf-8') as f:
                f.write(data)
            print(f"元のファイルを更新しました: {local_dic}")

        except FileNotFoundError:
            print(f"エラー: {local_dic} が見つかりません。")
        except Exception as e:
            print(f"処理中にエラーが発生しました: {e}")

