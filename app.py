from st_pages import Page, show_pages
import streamlit as st
st.set_page_config(layout="wide")
show_pages(
    [
        Page("room-sku-7day.py", "7日"),
        Page("room-sku-3day.py", "3日"),
        Page("room-sku-custom-day.py", "自选日期")

    ]
)
