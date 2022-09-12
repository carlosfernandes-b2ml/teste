import pandas as pd
import matplotlib.pyplot as plt


class DadoPessoal:
    dados: pd.DataFrame
    colaborador: str

    def __init__(self, dados: pd.DataFrame):
        self.dados = dados
        self.colaborador = self.dados['usuario'][0]

    def horas_dia(self):
        horas_dia = self.dados.groupby('data_inicial').sum().reset_index(level=0)
        horas_dia = self.ajustar_tempo(horas_dia)
        horas_dia = self.preencher_datas(horas_dia)
        horas_dia['duracao_total'] = horas_dia.apply(lambda linha: duracao(linha), axis=1)
        return horas_dia

    def horas_atividade(self):
        horas_atividade = self.dados.groupby('descricao').sum().reset_index(level=0)
        horas_atividade = self.ajustar_tempo(horas_atividade)
        horas_atividade['duracao_string'] = horas_atividade.apply(lambda linha: tempo_str(linha), axis=1)
        horas_atividade['duracao_total'] = horas_atividade.apply(lambda linha: duracao(linha), axis=1)
        return horas_atividade.sort_values(by=['duracao_total'], ascending=False).loc[:,['descricao', 'duracao_string']]


    @staticmethod
    def ajustar_tempo(df: pd.DataFrame):
        for index, row in df.iterrows():
            if row['duracao_segundos'] >= 60:
                row['duracao_minutos'] += int(row['duracao_segundos'] / 60)
                row['duracao_segundos'] = row['duracao_segundos'] % 60
            if row['duracao_minutos'] >= 60:
                row['duracao_horas'] += int(row['duracao_minutos'] / 60)
                row['duracao_minutos'] = row['duracao_minutos'] % 60

            df.at[index, 'duracao_segundos'] = row['duracao_segundos']
            df.at[index, 'duracao_minutos'] = row['duracao_minutos']
            df.at[index, 'duracao_horas'] = row['duracao_horas']
        return df

    @staticmethod
    def preencher_datas(df: pd.DataFrame) -> pd.DataFrame:
        dia_anterior = 0
        for index, row in df.iterrows():
            dia_atual = int(row['data_inicial'].split('/')[0])

            if dia_atual - dia_anterior > 1:
                for i in range(1, dia_atual - dia_anterior):
                    data_provisoria = f"{str(dia_anterior + i).zfill(2)}{row['data_inicial'][2:]}"
                    lista = [data_provisoria, 0, 0, 0]
                    df = df.append(pd.DataFrame([lista], columns=['data_inicial', 'duracao_horas', 'duracao_minutos',
                                                                  'duracao_segundos']))
        return df.sort_values(by=['data_inicial'])

    def gerar_grafico(self):
        horas_por_dia = self.horas_dia()
        horas_por_dia.plot(x='data_inicial', y='duracao_total', kind='bar', legend=False)

        plt.xticks(rotation=0, horizontalalignment="center")
        plt.xlabel("Data", fontdict={'fontsize':24})
        plt.ylabel("Horas Trabalhadas", fontdict={'fontsize':24})
        plt.savefig('grafico_01.png')

    def total_horas_recurso(self):
        total_horas = self.dados.groupby('usuario').sum().reset_index(level=0)
        total_horas = self.ajustar_tempo(total_horas)
        total_horas['duracao_string'] = total_horas.apply(lambda linha: tempo_str(linha), axis=1)
        total_horas['duracao_total'] = total_horas.apply(lambda linha: duracao(linha), axis=1)
        return total_horas.loc[:, ['usuario', 'duracao_string']]


def duracao(row):
    return row['duracao_horas'] + row['duracao_minutos'] / 60 + row['duracao_segundos'] / 3600

def tempo_str(row):
    return f"{row['duracao_horas']}:{str(row['duracao_minutos']).zfill(2)}:{str(row['duracao_segundos']).zfill(2)}"
