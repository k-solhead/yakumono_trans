import streamlit as st
import fitz # PyMuPDFをインポート
import pymupdf
import re
import sys


# pdfにハイライト注釈をつける関数
def pdf_insert(doc, search_text, input_text):
    highlight_color = (0, 1, 0)

    for page in doc:
        # ページ内で指定したテキストを検索し、矩形のリストを取得
        text_instances = page.search_for(search_text)
        # 見つかったすべてのテキストにハイlight注釈を追加
        for inst in text_instances:
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
                widget = fitz.Widget()
                widget.rect = rect
                widget.field_type = fitz.PDF_WIDGET_TYPE_COMBOBOX
                widget.field_flags = (
                    fitz.PDF_CH_FIELD_IS_COMBO
                    | fitz.PDF_CH_FIELD_IS_EDIT
                    | fitz.PDF_CH_FIELD_IS_COMMIT_ON_SEL_CHANGE  # update when focus changes
                )
                widget.field_name = dropdown_name
                widget.choice_values = options
                widget.border_color = (0.5, 0.5, 0.5) # 枠線の色 (グレー)
                widget.font_size = 8
                # ページにウィジェットを追加
                page.add_widget(widget)

# PDFファイルを開く
st.title("和文全角半角チェック")
st.write("日本語PDFファイルについての数字・記号の全角、半角が適切かどうか確認します")

uploaded_file = st.file_uploader("PDFファイルをアップロード", type="pdf")

if uploaded_file is not None:
    # pdf_bytes = uploaded_file.getvalue()
    st.success("ファイルがアップロードされました。")

    # アップロードされたファイルをバイトストリームとして読み込み、PyMuPDFで開く
    # `uploaded_file.read()`でファイル内容をバイトデータとして取得
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:

        # 全角半角変換
        replacement = {
	        '/':'／',		# 半角スラッシュを全角に
	        '\u003D':'\uFF1D',	# =	等号
	        '\u002B':'\uFF0B',	# +	足す
	        '\u002D':'\uFF0D',	# -	引く
	        '\u00D7':'\uFF0A',	# ×	掛ける(半角はアスタリスク)
	        '\u00F7':'\uFF0F',	# ÷	割る（スラッシュ）
	        '\u003C':'\uFF1C',	# <	小なり
	        '\u003E':'\uFF1E',	# >	大なり
	        '\u0028':'\uFF08',	# （	左丸カッコ
	        '\u0029':'\uFF09',	# ）	右丸カッコ
	        '\u005B':'\uFF3B',	# [	左角カッコ
	        '\u005D':'\uFF3D',	# ]	右角カッコ
	        '\u007B':'\uFF5B',	# {	左波カッコ
	        '\u007D':'\uFF5D',	# }	右波カッコ
	        '\u003A':'\uFF1A',	# :	コロン
	        '\u003B':'\uFF1B',	# ;	セミコロン
	        '\u0025':'\uFF05',	# %	パーセント
            '\uFF10':'\u0030',      #
            '\uFF11':'\uFF11',      #
            '\uFF12':'\uFF12',      #
            '\uFF13':'\uFF13',      #
            '\uFF14':'\uFF14',      #
            '\uFF15':'\uFF15',      #
            '\uFF16':'\uFF16',      #
            '\uFF17':'\uFF17',      #
            '\uFF18':'\uFF18',      #
            '\uFF19':'\uFF19',      #
        }
        for old,new in replacement.items():
            pdf_insert(doc, old, new)

        # 変更を新しいPDFファイルに保存
        output_pdf = "./output/output.pdf"
        doc.save(output_pdf, garbage=4, deflate=True, clean=True)
        st.success("処理が完了しました。ダウンロードボタンを推してください")

        # ダウンロードボタンを作成
        #st.download_button(
        #    label="PDFをダウンロード",
        #    data=doc,
        #    file_name="generated_document.pdf",
        #    mime="application/pdf"
        #)
        #print(f"ダウンロードしました。")
    #except Exception as e:
    #    st.error(f"PDFの処理中にエラーが発生しました: {e}")

with open("./output/output.pdf", "rb") as file:
    pdf_data = file.read()
# ダウンロードボタンを作成
st.download_button(
    label="PDFをダウンロード",
    data=pdf_data,
    file_name="generated_document.pdf",
    mime="application/pdf"
)

print(f"ダウンロードしました。")