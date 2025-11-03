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

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            # 後処理:
            # 1. ハイフンと直後の改行を削除して単語を結合
            #    (例: "docu-\nment" -> "document")
            text = re.sub(r'-\n', '', text)
    
            # 2. 残った余分な改行やスペースを調整する（必要に応じて）
            #    （例: "text.\nNext" -> "text. Next"）
            text = re.sub(r'\n', ' ', text) # 全ての改行をスペースに置換
            text = re.sub(r' +', ' ', text) # 複数のスペースを単一のスペースに置換

            words_list = re.findall(r'\b[a-z]+\b', text)
                                          
            # SpellChecker オブジェクトを作成
            # デフォルトの言語辞書を使用しない場合は language=None を指定
            # デフォルトの英語辞書にカスタムワードを追加する場合は language='en' (または他の言語) を指定
            spell = SpellChecker(language='en')
            
            # 追加したい単語のリスト
            custom_words = ['investee','investees','reinsurance','decarbonization','decarbonized','decarbonizing','materialities','work-life','worklife',\
                'iterating','quantitatively','largescale','decarbonize','decarbonized','decarbonization','reinsurance','quantification','timeframe','timeframes',\
                    'synergy','synergies','inviter','overhire','roadmaps','holistically','roadmaps','substitutability','montane','bushwalk','bushwalks','stably',\
                        'isomerized','genotypes','lightweighting','unavailability','preforms','biochar','workforces','agilely','yearround','divestment','jobsites',\
                            'jobsite','bauma','remanufacturing','workstyle','afforestation','systemization','netzero','decision-making','decision-making','decision making',\
                                'heatwaves','highquality','colorings','mitigatory','afterward','polyphenols','lipolytic','quercetin','biotechnologies','worldclass','world-class',\
                                    'collaboratively','biodiverse','onboarding','on-boarding','unallocated','megatrend','megatrends','bioplastics','bioplastic','backcasting',\
                                        'stepwise','reproducibility','usability']
            # load_words メソッドを使用して単語リストを読み込み、頻度リストを生成
            spell.word_frequency.load_words(custom_words)
            misspelled = spell.unknown(words_list)
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