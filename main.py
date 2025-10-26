import streamlit as st

def main():

    top_page = st.Page(
        page = "contents/en.py", title="SpellCheck", default=True
    )
    wabun = st.Page(
        page = "contents/ja.py", title="Zenkaku"
    )
    yakumono = st.Page(
        page = "contents/yakumono.py", title="Yakumono"
    )

    pg = st.navigation([top_page, wabun, yakumono])
    pg.run()

if __name__ == "__main__":
    main()
