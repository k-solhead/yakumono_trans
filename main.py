import streamlit as st

def main():

    top_page = st.Page(
        page = "contents/spell.py", title="SpellCheck", default=True
    )
    English = st.Page(
        page = "contents/en.py", title="English"
    )
    Japanese = st.Page(
        page = "contents/ja.py", title="Japanese"
    )
    Dictionary = st.Page(
        page = "contents/dictionary.py", title="Dictionary"
    )

    pg = st.navigation([top_page, English, Japanese, Dictionary])
    pg.run()

if __name__ == "__main__":
    main()
