import streamlit as st
#import fitz # PyMuPDFをインポート
import pymupdf
from spellchecker import SpellChecker # Using pyspellchecker instead
import re
import sys

count = 0
# 分かち書きの英単語から指定された文字列を検索する関数
#　　検索文字列を含む完全な単語の座標の配列をリスト化
def mark_word(page, text):
    wlist = page.get_text("words", delimiters=None)  # make the word list
    rlist = []
    for w in wlist:  # scan through all words on page
        if text in w[4]:  # w[4] is the word's string
            r = pymupdf.Rect(w[:4])  # make rect from word bbox
            rlist.append(r)
    return rlist

# pdfにハイライト注釈をつける関数
def pdf_insert(doc, search_text, input_text, replace):
    highlight_color = (0, 1, 0)

    for page in doc:
        # ページ内で指定したテキストを検索し、矩形のリストを取得
        text_instances = page.search_for(search_text)
        # 見つかったすべてのテキストにハイlight注釈を追加
        for inst in text_instances:
            if (inst in mark_word(page, search_text)) | replace:
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
                    global count
                    count += 1
                    widget.field_name = dropdown_name + str(count)
                    widget.choice_values = options
                    widget.border_color = (0.5, 0.5, 0.5) # 枠線の色 (グレー)
                    widget.font_size = 8
                    # ページにウィジェットを追加
                    page.add_widget(widget)

# PDFファイルを開く
st.title("SpellCheck")
st.write("英語PDFファイルのスペルチェックやフォント調整をします")

uploaded_file = st.file_uploader("PDFファイルをアップロード", type="pdf")

if uploaded_file is not None:
    # pdf_bytes = uploaded_file.getvalue()
    st.success("ファイルがアップロードされました。")

    # アップロードされたファイルをバイトストリームとして読み込み、PyMuPDFで開く
    # `uploaded_file.read()`でファイル内容をバイトデータとして取得
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:

        # スペルチェック
        spell = SpellChecker() # Initialize pyspellchecker

        for page in doc:
            text = page.get_text()
            word_list = re.findall(r'\b[a-z]+\b', text.lower())
            # find those words that may be misspelled
            misspelled = spell.unknown(word_list)
            for word in misspelled:
                print(word)
                pdf_insert(doc, word, spell.correction(word), False)

        # 全角半角変換
        replacement = {
            '\u3000':'\u0020',      # 全角空白を半角空白へ
            '. \n':'.\n',           # 文末の半角空白を削除（改行LFの場合）
            '. \r\n':'.\r\n',       # 文末の半角空白を削除（改行CRLFの場合）
            '\u30FB':'\u2022',      # 中黒をビュレットに変換
            '\uFF01':'\u0021',      # !
            '\uFF02':'\u0022',      # "
            '\uFF03':'\u0023',      # #
            '\uFF04':'\u0024',      # $
            '\uFF05':'\u0025',      # %
            '\uFF06':'\u0026',      # &
            '\uFF07':'\u0027',      # '
            '\uFF08':'\u0028',      # (
            '\uFF09':'\u0029',      # )
            '\uFF0A':'\u002A',      # *
            '\uFF0B':'\u002B',      # +
            '\uFF0C':'\u002C',      # ,
            '\uFF0D':'\u002D',      # -
            '\uFF0E':'\u002E',      # .
            '\uFF0F':'\u002F',      # /
            '\uFF10':'\u0030',      # 0
            '\uFF11':'\u0031',      # 1
            '\uFF12':'\u0032',      # 2
            '\uFF13':'\u0033',      # 3
            '\uFF14':'\u0034',      # 4
            '\uFF15':'\u0035',      # 5
            '\uFF16':'\u0036',      # 6
            '\uFF17':'\u0037',      # 7
            '\uFF18':'\u0038',      # 8
            '\uFF19':'\u0039',      # 9
            '\uFF1A':'\u003A',      # :
            '\uFF1B':'\u003B',      # ;
            '\uFF1C':'\u003C',      # <
            '\uFF1D':'\u003D',      # =
            '\uFF1E':'\u003E',      # >
            '\uFF1F':'\u003F',      # ?
            '\uFF20':'\u0040',      # @
            '\uFF21':'\u0041',      # A
            '\uFF22':'\u0042',      # B
            '\uFF23':'\u0043',      # C
            '\uFF24':'\u0044',      # D
            '\uFF25':'\u0045',      # E
            '\uFF26':'\u0046',      # F
            '\uFF27':'\u0047',      # G
            '\uFF28':'\u0048',      # H
            '\uFF29':'\u0049',      # I
            '\uFF2A':'\u004A',      # J
            '\uFF2B':'\u004B',      # K
            '\uFF2C':'\u004C',      # L
            '\uFF2D':'\u004D',      # M
            '\uFF2E':'\u004E',      # N
            '\uFF2F':'\u004F',      # O
            '\uFF30':'\u0050',      # P
            '\uFF31':'\u0051',      # Q
            '\uFF32':'\u0052',      # R
            '\uFF33':'\u0053',      # S
            '\uFF34':'\u0054',      # T
            '\uFF35':'\u0055',      # U
            '\uFF36':'\u0056',      # V
            '\uFF37':'\u0057',      # W
            '\uFF38':'\u0058',      # X
            '\uFF39':'\u0059',      # Y
            '\uFF3A':'\u005A',      # Z
            '\uFF3B':'\u005B',      # [
            '\uFF3C':'\u005C',      # \
            '\uFF3D':'\u005D',      # ]
            '\uFF3E':'\u005E',      # ^
            '\uFF3F':'\u005F',      # _
            '\uFF40':'\u0060',      # `
            '\uFF41':'\u0061',      # a
            '\uFF42':'\u0062',      # b
            '\uFF43':'\u0063',      # c
            '\uFF44':'\u0064',      # d
            '\uFF45':'\u0065',      # e
            '\uFF46':'\u0066',      # f
            '\uFF47':'\u0067',      # g
            '\uFF48':'\u0068',      # h
            '\uFF49':'\u0069',      # i
            '\uFF4A':'\u006A',      # j
            '\uFF4B':'\u006B',      # k
            '\uFF4C':'\u006C',      # l
            '\uFF4D':'\u006D',      # m
            '\uFF4E':'\u006E',      # n
            '\uFF4F':'\u006F',      # o
            '\uFF50':'\u0070',      # p
            '\uFF51':'\u0071',      # q
            '\uFF52':'\u0072',      # r
            '\uFF53':'\u0073',      # s
            '\uFF54':'\u0074',      # t
            '\uFF55':'\u0075',      # u
            '\uFF56':'\u0076',      # v
            '\uFF57':'\u0077',      # w
            '\uFF58':'\u0078',      # x
            '\uFF59':'\u0079',      # y
            '\uFF5A':'\u007A',      # z
            '\uFF5B':'\u007B',      # {
            '\uFF5C':'\u007C',      # |
            '\uFF5D':'\u007D',      # }
            '\uFF5E':'\u007E',      # ~
        }
        for old,new in replacement.items():
            pdf_insert(doc, old, new, True)

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
