from src.dashboard.login import login_view
import streamlit as st
from src.dashboard.navigator import nav
from src.dashboard.setup import setup
from src.logs.logger import configLogger


def main():
    """
    Função principal do aplicativo Streamlit.
    para rodar o aplicativo, execute o seguinte comando:
    streamlit run main_dash.py
    :return:
    """
    configLogger()

    if not st.session_state.get('logged_in', False):
        #Escreve inúmeras vezes no loop
        # logging.debug('acessando login')
        login_view()
    else:
        #Escreve inúmeras vezes no loop
        # logging.debug('acessando dashboard')
        setup()
        nav()

if __name__ == "__main__":
    main()
