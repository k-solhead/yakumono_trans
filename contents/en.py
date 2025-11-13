import streamlit as st
import docx
from io import BytesIO
import os
import re

output_word = "./output/output.docx"
replacement = {
    '\u3000':'\u0020',      # 全角空白を半角空白へ
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
    '\ ':'¥',
    '("':'(“',
    '\\':'¥',
    "'":"’",
    '" ':'”\s',
    ' "':'\s“',
    '")':'”)',
    '".':'”.',
    '."':'.”',
    '・\t':'• ',
    '：／／':'://',
    'jp／':'jp/',
    ' )':')',
    ' . ':'. ',
    ' , ':', ',
    '" ':'” ',
    '( ':'(',
    "' ":"’ ",
    "'":"’",
    "• ":"•   ",
    '） ':'）',
    ' （':'（',
    '."':'.”',
    "' ":"’ ",
    ' 、':'、',
    '。 ':'。',
    'com／':'com/',
    'net／':'net/',
    ' 年':'年',
    ' 日':'日',
    ' 月':'月',
    '、 ':'、',
    '： ':'：',
    ' ：':'：',
    ' 円':'円',
    ' 時':'時',
    ' 分':'分',
    ' 百万円':'百万円',
    ' 億円':'億円',
    ' ％':'％',
    ' %':'%',
    ',"':',”',
    '  ':' ',
    '",':'”,',
    ' 」':'」',
    '－':'–',
    '（ ':'（',
    ' （':'（',
    '） ':'）',
    '( ':'(',
    ' "':' “',
    'http：//':'http://',
    '：//':'://',
    'https：':'https:',
    '」 ':'」',
    ' 「':'「',
    '］ ':'］',
    'Source：':'Source: ',
    '（Billions）':' (Billions) ',
    'Note：':'Note: ',
    '（Thousands）':'(Thousands) ',
    '（Millions）':' (Millions) ',
    '〜 ':'〜',
    '\t -':'\t\u2013',
    '¥-':'¥–',
    '$ ':'$',
    '➢':'>',
    '\u3000\t':'\t',
    '\s\\':'\s¥',
    '\s\s\s':'\s',
    '\t\\':'\t¥',
}

st.title("英文文字・記号修正")
st.write("英文フォントの半角への修正や約物の自動変換をします")

# st.file_uploaderウィジェットの作成
# type引数で受け付けるファイルの形式を'.docx'に限定
uploaded_file = st.file_uploader("Wordファイル（.docx）をアップロード", type=['docx'])

# ファイルがアップロードされた場合の処理
if uploaded_file is not None:
    file_name = os.path.splitext(uploaded_file.name)[0]  # アップロードされたファイル名を取得
    st.success("ファイルが正常にアップロードされました。")

    # BytesIOでアップロードされたファイルを扱う
    doc_file = BytesIO(uploaded_file.getvalue())

    try:
        # python-docxでWordドキュメントを開く
        doc = docx.Document(doc_file)
        # re.DOTALL は改行を含む任意のマッチングを可能にする場合に有用
        pattern = re.compile(r'\.\s+', re.DOTALL)
        for para in doc.paragraphs:
            t = re.sub(pattern, '.', para.text)
            for old,new in replacement.items():
                t = t.replace(old, new)
            para.text = t

        # 変更を新しいPDFファイルに保存
        doc.save(output_word)
        st.success("処理が完了しました")

        # ドキュメントの内容を表示
        #st.subheader("処理されたWordファイルの内容")
        
        # ドキュメント内の各段落を読み込んで表示
        #for para in doc.paragraphs:
        #    st.write(para.text)
        st.success("ダウンロードボタンを押してください")
        with open(output_word, "rb") as file:
            word_data = file.read()
            # ダウンロードボタンを作成
            st.download_button(
                label="Word文書をダウンロード",
                data=word_data,
                file_name=file_name+"_chk.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", # WordファイルのMIMEタイプ
            )
        print(f"ダウンロードしました。")

        
    except Exception as e:
        st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
else:
    st.info("ファイルをアップロードしてください。")            
