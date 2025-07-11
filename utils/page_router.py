import importlib
import streamlit as st

def show_page(page_name: str):
    try:
        page_module = importlib.import_module(f"pages.{page_name}")
        page_module.main()
    except ModuleNotFoundError:
        st.error(f"Página '{page_name}' não encontrada.")
    except AttributeError:
        st.error(f"A página '{page_name}' não possui a função 'main()'.")