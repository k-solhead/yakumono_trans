
import streamlit as st
import docx
from io import BytesIO
import os
import re

output_word = "./output/output.docx"
replacement = {
    '/':'／',		# 半角スラッシュを全角に
    '\u0021':'\uFF01',      # !　(全角)
    '\u0022':'\uFF02',      # "　(全角)
    '\u0023':'\uFF03',      # #　(全角)
    '\u0024':'\uFF04',      # $　(全角)
    '\u0025':'\uFF05',      # %　(全角)
    '\u0026':'\uFF06',      # &　(全角)
    '\u0027':'\uFF07',      # '　(全角)
    '\u0028':'\uFF08',      # (　(全角)
    '\u0029':'\uFF09',      # )　(全角)
    '\u002A':'\uFF0A',      # *　(全角)
    '\u002B':'\uFF0B',      # +　(全角)
    '\u002C':'\uFF0C',      # ,　(全角)
    '\u002D':'\uFF0D',      # -　(全角)
    '\u002E':'\uFF0E',      # .　(全角)
    '\u002F':'\uFF0F',      # /　(全角)
    '\uFF10':'\u0030',      # 0　(半角)
    '\uFF11':'\u0031',      # 1　(半角)
    '\uFF12':'\u0032',      # 2　(半角)
    '\uFF13':'\u0033',      # 3　(半角)
    '\uFF14':'\u0034',      # 4　(半角)
    '\uFF15':'\u0035',      # 5　(半角)
    '\uFF16':'\u0036',      # 6　(半角)
    '\uFF17':'\u0037',      # 7　(半角)
    '\uFF18':'\u0038',      # 8　(半角)
    '\uFF19':'\u0039',      # 9　(半角)
    '\u003A':'\uFF1A',      # :　(全角)
    '\u003B':'\uFF1B',      # ;　(全角)
    '\u003C':'\uFF1C',      # <　(全角)
    '\u003D':'\uFF1D',      # =　(全角)
    '\u003E':'\uFF1E',      # >　(全角)
    '\u003F':'\uFF1F',      # ?　(全角)
    '\u0040':'\uFF20',      # @　(全角)
    '\uFF21':'\u0041',      # A　(半角)
    '\uFF22':'\u0042',      # B　(半角)
    '\uFF23':'\u0043',      # C　(半角)
    '\uFF24':'\u0044',      # D　(半角)
    '\uFF25':'\u0045',      # E　(半角)
    '\uFF26':'\u0046',      # F　(半角)
    '\uFF27':'\u0047',      # G　(半角)
    '\uFF28':'\u0048',      # H　(半角)
    '\uFF29':'\u0049',      # I　(半角)
    '\uFF2A':'\u004A',      # J　(半角)
    '\uFF2B':'\u004B',      # K　(半角)
    '\uFF2C':'\u004C',      # L　(半角)
    '\uFF2D':'\u004D',      # M　(半角)
    '\uFF2E':'\u004E',      # N　(半角)
    '\uFF2F':'\u004F',      # O　(半角)
    '\uFF30':'\u0050',      # P　(半角)
    '\uFF31':'\u0051',      # Q　(半角)
    '\uFF32':'\u0052',      # R　(半角)
    '\uFF33':'\u0053',      # S　(半角)
    '\uFF34':'\u0054',      # T　(半角)
    '\uFF35':'\u0055',      # U　(半角)
    '\uFF36':'\u0056',      # V　(半角)
    '\uFF37':'\u0057',      # W　(半角)
    '\uFF38':'\u0058',      # X　(半角)
    '\uFF39':'\u0059',      # Y　(半角)
    '\uFF3A':'\u005A',      # Z　(半角)
    '\u005B':'\uFF3B',      # [　(全角)
    '\u005C':'\uFF3C',      # \　(全角)
    '\u005D':'\uFF3D',      # ]　(全角)
    '\u005E':'\uFF3E',      # ^　(全角)
    '\u005F':'\uFF3F',      # _　(全角)
    '\u0060':'\uFF40',      # `　(全角)
    '\uFF41':'\u0061',      # a　(半角)
    '\uFF42':'\u0062',      # b　(半角)
    '\uFF43':'\u0063',      # c　(半角)
    '\uFF44':'\u0064',      # d　(半角)
    '\uFF45':'\u0065',      # e　(半角)
    '\uFF46':'\u0066',      # f　(半角)
    '\uFF47':'\u0067',      # g　(半角)
    '\uFF48':'\u0068',      # h　(半角)
    '\uFF49':'\u0069',      # i　(半角)
    '\uFF4A':'\u006A',      # j　(半角)
    '\uFF4B':'\u006B',      # k　(半角)
    '\uFF4C':'\u006C',      # l　(半角)
    '\uFF4D':'\u006D',      # m　(半角)
    '\uFF4E':'\u006E',      # n　(半角)
    '\uFF4F':'\u006F',      # o　(半角)
    '\uFF50':'\u0070',      # p　(半角)
    '\uFF51':'\u0071',      # q　(半角)
    '\uFF52':'\u0072',      # r　(半角)
    '\uFF53':'\u0073',      # s　(半角)
    '\uFF54':'\u0074',      # t　(半角)
    '\uFF55':'\u0075',      # u　(半角)
    '\uFF56':'\u0076',      # v　(半角)
    '\uFF57':'\u0077',      # w　(半角)
    '\uFF58':'\u0078',      # x　(半角)
    '\uFF59':'\u0079',      # y　(半角)
    '\uFF5A':'\u007A',      # z　(半角)
    '\u007B':'\uFF5B',      # {　(全角)
    '\u007C':'\uFF5C',      # |　(全角)
    '\u007D':'\uFF5D',      # }　(全角)
    '\u007E':'\uFF5E',      # ~　(全角)
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

st.title("和文文字・記号修正")
st.write("和文フォントの全角・半角への修正や約物の自動変換をします")

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
        for para in doc.paragraphs:
            t = para.text
            for old,new in replacement.items():
                t = t.replace(old, new)
            para.text = t

        # 変更を新しいPDFファイルに保存
        # output_word = "./output/output.docx"
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
            
