
import streamlit as st
import docx
from docx.enum.text import WD_COLOR_INDEX
from io import BytesIO
import os
import re

def zen_to_han(char):
    """全角英数記号を半角に変換"""
    cp = ord(char)
    # 全角英数記号 (FF01-FF5E) → 半角 (0021-007E)
    if 0xFF01 <= cp <= 0xFF5E:
        return chr(cp - 0xFEE0)
    # 全角スペース → 半角スペース
    if cp == 0x3000:
        return ' '
    return char

def normalize_url_email(text):
    """URL・メールアドレス内の全角文字を半角に変換"""
    # URL（全角文字混在対応）
    url_pattern = r'[\uFF48\uFF28hH][\uFF54\uFF34tT][\uFF54\uFF34tT][\uFF50\uFF30pP][\uFF53\uFF33sS]?[\uFF1A：:][\uFF0F／/][\uFF0F／/][^\s\u3000]+'
    # メールアドレス（全角文字混在対応）
    email_pattern = r'[\w\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19][\w.\-\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19\uFF0E\uFF0D]*[\uFF20@][\w\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19][\w.\-\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19\uFF0E\uFF0D]*'
    combined = f'({url_pattern})|({email_pattern})'
    def replace_match(m):
        return ''.join(zen_to_han(c) for c in m.group(0))
    return re.sub(combined, replace_match, text)

# URLパターン（全角スラッシュ・コロン混在対応）
_url_re = re.compile(r'https?[:\uFF1A][/\uFF0F]{2}[^\s\u3000]+')

def protect_urls(text, func):
    """テキスト中のURLを一時的にプレースホルダーに置き、funcを適用後に復元。URL内の全角スラッシュ・コロンは半角に変換"""
    urls = []
    def save(m):
        url = m.group(0).replace('\uFF0F', '/').replace('\uFF1A', ':')
        urls.append(url)
        return f'\x00URL{len(urls)-1}\x00'
    text = _url_re.sub(save, text)
    text = func(text)
    for i, url in enumerate(urls):
        text = text.replace(f'\x00URL{i}\x00', url)
    return text

def apply_slash_colon(text):
    """/→／、:→：を変換（URL外）"""
    text = text.replace('/', '\uff0f')
    text = text.replace(':', '\uff1a')
    return text

# ※/＊/*+数字パターン（ハイライト対象）
note_pattern = re.compile(r'[\u203B\uFF0A\*][0-9\uFF10-\uFF19]+')

def apply_note_highlight_per_run(para):
    """各run内の※/*/＊+数字パターンを別runに分けてハイライトする（run書式を保持）"""
    if not any(note_pattern.search(run.text) for run in para.runs):
        return
    new_runs_data = []
    for run in para.runs:
        text = run.text
        is_bold = run.bold
        is_italic = run.italic
        cur_highlight = run.font.highlight_color
        matches = list(note_pattern.finditer(text))
        if not matches:
            if text:
                new_runs_data.append((text, is_bold, is_italic, cur_highlight))
            continue
        last_end = 0
        for m in matches:
            before = text[last_end:m.start()]
            if before:
                new_runs_data.append((before, is_bold, is_italic, cur_highlight))
            new_runs_data.append((m.group(0), is_bold, is_italic, WD_COLOR_INDEX.TURQUOISE))
            last_end = m.end()
        remaining = text[last_end:]
        if remaining:
            new_runs_data.append((remaining, is_bold, is_italic, cur_highlight))
    for run in para.runs:
        run.text = ''
    if not new_runs_data:
        return
    if para.runs:
        text, is_bold, is_italic, highlight = new_runs_data[0]
        r = para.runs[0]
        r.text = text
        r.bold = is_bold
        r.italic = is_italic
        if highlight is not None:
            r.font.highlight_color = highlight
    for text, is_bold, is_italic, highlight in new_runs_data[1:]:
        new_r = para.add_run(text)
        new_r.bold = is_bold
        new_r.italic = is_italic
        if highlight is not None:
            new_r.font.highlight_color = highlight

output_word = "./output/output.docx"
os.makedirs(os.path.dirname(output_word), exist_ok=True)

replacement = {
    '\u0021':'\uFF01',      # !　(全角)
    '\u0022':'\uFF02',      # "　(全角)
    '\u0023':'\uFF03',      # #　(全角)
    '\u0024':'\uFF04',      # $　(全角)
    '\uFF05':'\u0025',      # %　(全角→半角)
    '\u0026':'\uFF06',      # &　(全角)
    '\u0027':'\uFF07',      # '　(全角)
    '\u0028':'\uFF08',      # (　(全角)
    '\u0029':'\uFF09',      # )　(全角)
    '\uFF0A':'\u002A',      # *　(全角)
    '\u002B':'\uFF0B',      # +　(全角)
    '\uFF0C':'\u002C',      # ,　(半角)　位取りのコンマ
    '\u002D':'\uFF0D',      # -　(全角)
    '\uFF0E':'\u002E',      # .　(半角)　小数点
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
    '\u33A1':'m2',          # 機種依存文字（平方メートル）
    '\u33A5':'m3',          # 機種依存文字（立法メートル）
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

st.title("テキスト整形（和文）")
st.write("和文フォントの全角・半角への修正や約物の自動変換をします")

option = st.radio("Word文書かテキストか整形対象を選択してください", ("Word文書", "テキスト文書"))

if option == "テキスト文書":
    if "text" not in st.session_state:
        st.session_state.text = ""
    st.session_state.text = st.text_area("テキストを貼りつけてください", height=300, placeholder="ここに貼りつけてください")
    
    if st.button("実行する"):    
        try:
            text = st.session_state.text
            text = normalize_url_email(text)
            for old,new in replacement.items():
                text = text.replace(old, new)
            text = protect_urls(text, apply_slash_colon)
            text = re.sub(r'\s*(\d+)\s*', r'\1', text)
        
            st.success("処理が完了しました。下記テキストをコピペしてください")
            with st.container(border=True):
                st.text(text)
            
        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
            
else:
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
                # Run単位の処理：テキスト置換 + 数字前後空白除去
                for run in para.runs:
                    t = run.text
                    for old, new in replacement.items():
                        t = t.replace(old, new)
                    t = re.sub(r'\s*(\d+)\s*', r'\1', t)
                    run.text = t

                # 段落全体でURL正規化 + スラッシュ・コロン変換（URL跨ぎrun対応）
                if para.runs:
                    full_text = ''.join(run.text for run in para.runs)
                    full_text = normalize_url_email(full_text)
                    full_text = protect_urls(full_text, apply_slash_colon)
                    idx = 0
                    for run in para.runs:
                        run_len = len(run.text)
                        run.text = full_text[idx:idx + run_len]
                        idx += run_len

                # Run単位の太字・斜体ハイライト
                for run in para.runs:
                    if run.bold:
                        run.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    if run.italic:
                        run.font.highlight_color = WD_COLOR_INDEX.PINK

                # ※/*+数字パターンのハイライト（run単位で処理）
                apply_note_highlight_per_run(para)

                # 箇条書きスタイルの解除とビュレット挿入
                is_list = para.style.name.startswith('List') or para._element.pPr is not None and para._element.pPr.find(
                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr') is not None
                if is_list:
                    if para.runs:
                        para.runs[0].text = '• ' + para.runs[0].text
                    # numPr（ナンバリング属性）を削除して箇条書き設定を解除
                    if para._element.pPr is not None:
                        numPr = para._element.pPr.find(
                            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr')
                        if numPr is not None:
                            para._element.pPr.remove(numPr)
                    para.style = doc.styles['Normal']

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
                    on_click="ignore" # 再実行を無視する設定
                )
            print(f"ダウンロードしました。")
        
        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {e}")
    else:
        st.info("ファイルをアップロードしてください。")
            
