from model import *
from csv_reader import *
import matplotlib.pyplot as plt
from relatorio_pdf import *
from control import *

if __name__ == '__main__':
    controller = Control()
    controller.run()
    plt.rcParams["figure.figsize"] = [30, 6]
    plt.rcParams.update({'font.size': 16})
    fig = plt.figure()
    arquivo = 'teste_02.csv'
    dados = generate_dataframe(arquivo)
    relatorio = DadoPessoal(dados)
    # Relatorio().capa(relatorio.total_horas_recurso().append(relatorio.total_horas_recurso()))
    Relatorio().pagina_colaborador('grafico_01.png', relatorio.horas_atividade(), relatorio.total_horas_recurso())
    print('')
