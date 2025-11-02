import streamlit as st
import pymupdf
from spellchecker import SpellChecker # Using pyspellchecker instead
import re
import sys

highlight_color = (0, 1, 0)
output_pdf = "./output/output.pdf"
count = 0

# 分かち書きの英単語から指定された文字列を検索する関数
# 検索文字列を含む完全な単語の座標の配列をリスト化
def mark_word(page, text):
    wlist = page.get_text("words", delimiters=None)  # make the word list
    rlist = []
    for w in wlist:  # scan through all words on page
        if text in w[4]:  # w[4] is the word's string
            r = pymupdf.Rect(w[:4])  # make rect from word bbox
            rlist.append(r)
    return rlist

# PDFファイルを開く
st.title("SpellCheck")
st.write("英語PDFファイルのスペルチェックをします")

uploaded_file = st.file_uploader("PDFファイルをアップロード", type="pdf")

if uploaded_file is not None:
    st.success("ファイルがアップロードされました。")
    
    try:
        # アップロードされたファイルをバイトストリームとして読み込み、PyMuPDFで開く
        # `uploaded_file.read()`でファイル内容をバイトデータとして取得
        doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")   

        for page in doc:
            text = page.get_text()
            text_nohyphen = text.replace('-','')
            word_list = re.findall(r'\b[a-z]+\b', text)
                              
            # find those words that may be misspelled
            spell = SpellChecker() # Initialize pyspellchecker
            misspelled = spell.unknown(word_list)
            for word in misspelled:
                print(word)
                input_text = spell.correction(word)
                # ページ内で指定したテキストを検索し、矩形のリストを取得
                text_instances = page.search_for(word)
                # 見つかったすべてのテキストにハイlight注釈を追加
                for inst in text_instances:
                    if inst in mark_word(page, word):
                        annot = page.add_highlight_annot(inst)
                        annot.set_colors(stroke=highlight_color)
                        annot.update()
                        # プルdownメニューの追加
                        dropdown_name = "status_select"  # フィールド名
                        # Changed options format back to a list of strings
                        options = [input_text]

                        # プルdownを配置する座標とサイズ (左上x, 左上y, 右下x, 右上y)
                        rect = inst + (0, 10, 0, 10)

                        # Check if input_text is not empty before adding the widget
                        if input_text:
                            # ウィジェット（プルdownメニュー）を作成
                            widget = pymupdf.Widget()
                            widget.rect = rect
                            widget.field_type = pymupdf.PDF_WIDGET_TYPE_COMBOBOX
                            widget.field_flags = (
                                pymupdf.PDF_CH_FIELD_IS_COMBO
                                | pymupdf.PDF_CH_FIELD_IS_EDIT
                                | pymupdf.PDF_CH_FIELD_IS_COMMIT_ON_SEL_CHANGE  # update when focus changes
                            )
                            count += 1
                            widget.field_name = dropdown_name + str(count)
                            widget.choice_values = options
                            widget.border_color = (0.5, 0.5, 0.5) # 枠線の色 (グレー)
                            widget.font_size = 8
                            # ページにウィジェットを追加
                            page.add_widget(widget)

        # 変更を新しいPDFファイルに保存
        doc.save(output_pdf, garbage=4, deflate=True, clean=True)
        doc.close()
        st.success("処理が完了しました")
        
        st.success("ダウンロードボタンを押してください")        
        with open(output_pdf, "rb") as file:
            pdf_data = file.read()
            # ダウンロードボタンを作成
            st.download_button(
                label="PDFをダウンロード",
                data=pdf_data,
                file_name="spellcheck.pdf",
                mime="application/pdf"
            )
        print(f"ダウンロードしました。")
        
    except Exception as e:
        st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
else:
    st.info("ファイルをアップロードしてください。")