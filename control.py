from datetime import datetime
from os import listdir
from os.path import isfile, join
from constantes import *

class Control:
    """
    O funcionamento do sistema é bem simples, são listados os arquivos que contém os dados dos colaboradores.
    Após isso, são gerados arquivos temporários (gráficos e pdfs para cada colaborador).
    Finalmente os pdfs sofrem merge e são enviados para a pasta de saída
    """

    def run(self):
        print(f'{datetime.now().strftime("%H:%M:%S")}\tINICIO DO SERVIÇO')
        entradas = [file for file in self.listar_entradas() if file.endswith('.csv')]
        print(entradas)

    def listar_entradas(self):
        return [f for f in listdir(PASTA_ENTRADA) if isfile(join(PASTA_ENTRADA, f))]