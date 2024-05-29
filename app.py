from st_pages import Page, show_pages
import streamlit as st
st.set_page_config(layout="wide")
show_pages(
    [
        Page("room-sku.py", "测试")

    ]
)
