import requests
import dotenv
import os
import streamlit as st
from pprint import pprint


def fazer_request(url, params = None):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro: {e}')
        resultado = None
    else:
        resultado = resposta.json()
    return resultado

def pegar_tempo_para_local(local):
    # ler o arquivo .env
    dotenv.load_dotenv()
    # acessar variável de ambiente
    token = os.environ['OPENWEATHER_TOKEN']

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid' : token,
        'q' : local,
        'units' : 'metric',
        'lang' : 'pt_br'
    }
    dados_tempo = fazer_request(url=url, params=params)
    return dados_tempo

def main():
    st.title('Web App do Tempo')
    st.write('Fonte: OpenWeather (https://openweathermap.org)')
    local = st.text_input('Busque uma cidade:')
    if not local:
        st.stop()
    dados_tempo = pegar_tempo_para_local(local=local)
    if not dados_tempo:
        st.warning(f'Dados não encontrados para a cidade {local}')
        st.stop()
    clima_atual = dados_tempo['weather'][0]['description']
    temperatura = dados_tempo['main']['temp']
    sensacao_termica = dados_tempo['main']['feels_like']
    umidade = dados_tempo['main']['humidity']
    cobertura_nuvens = dados_tempo['clouds']['all']
    
    st.metric(label='Tempo Atual', value=clima_atual)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f'Temperatura', value=f'{temperatura} °C')
        st.metric(label=f'Sensação térmica', value=f'{sensacao_termica} °C')
    with col2:
        st.metric(label='Umidade', value=f'{umidade} %')
        st.metric(label='Cobertura de nuvens', value=f'{cobertura_nuvens} %')

if __name__ == '__main__':
    main()
