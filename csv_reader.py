import pandas as pd
from datetime import datetime


def generate_dataframe(path: str) -> pd.DataFrame:
    dados = []
    with open(path, 'r', encoding='iso-8859-1', errors='ignore') as file:
        file.readline()
        linha = file.readline()

        while linha:
            linha = linha.encode('iso-8859-1').decode('utf8')
            linha = linha.split(',')

            dicionario = {
                'usuario': linha[0],
                'email': linha[1],
                'cliente': linha[2],
                'projeto': linha[3],
                'atividade': linha[4],
                'descricao': linha[5],
                'cobrado': linha[6],
                'data_inicial': datetime.strptime(linha[7], '%Y-%m-%d').strftime("%d/%m"),
                'hora_inicial': datetime.strptime(linha[8], '%H:%M:%S'),
                'data_final': datetime.strptime(linha[9], '%Y-%m-%d'),
                'hora_final': datetime.strptime(linha[10], '%H:%M:%S'),
                'duracao_horas': int(linha[11].split(':')[0]),
                'duracao_minutos': int(linha[11].split(':')[1]),
                'duracao_segundos': int(linha[11].split(':')[2])
            }
            dados.append(dicionario)

            linha = file.readline()

    return pd.DataFrame(dados)
