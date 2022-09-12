from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime
from constantes import *
import pandas as pd


class Relatorio:
    def capa(self, horas_recurso: pd.DataFrame):
        data = datetime.now()
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        cnv = canvas.Canvas("capa.pdf", pagesize=A4)
        self.desenhar_layout_basico(cnv)
        cnv.setFont("Helvetica-Bold", 16)

        cnv.drawCentredString(A4[0] / 2, A4[1] - 150, 'Relatório de Horas Trabalhadas')
        cnv.setFont("Helvetica", 12)
        cnv.drawRightString(A4[0] - 10, A4[1] - 200,
                            f'Relatório referente ao mês de {meses[data.month]} de {data.year}.')
        cnv.drawString(80, A4[1] - 260,
                       'Este relatório consiste na documentação e cobrança das horas trabalhadas, pelos ')
        cnv.drawString(80, A4[1] - 280,
                       'desenvolvedores disponibilizados pela contratada B2ML Sistemas, nas atividades ')
        cnv.drawString(80, A4[1] - 300, 'solicitadas pela contratante.')
        cnv.drawCentredString(A4[0] / 2, A4[1] - 430, 'Projeto Vooo - Total de Horas = 123:45:23')

        data = [['RECURSO', 'TOTAL DE HORAS']]

        for index, row in horas_recurso.iterrows():
            data.append([row['usuario'], row['duracao_string']])
        f = Table(data, colWidths=[150, 120], rowHeights=20)
        style = [
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ]
        f.setStyle(style)
        f.wrapOn(cnv, 50, 300)
        f.drawOn(cnv, A4[0] / 2 - 130, A4[1] - 500)

        cnv.save()
        return 0

    def pagina_colaborador(self, grafico, dados: pd.DataFrame, dados_colaborador: pd.DataFrame = None):
        # Primeira página
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        cnv = canvas.Canvas("pagina_teste.pdf", pagesize=A4)
        self.desenhar_layout_basico(cnv)
        cnv.setFont("Helvetica-Bold", 16)

        dados_colaborador = dados_colaborador.iloc[0, :]
        cnv.drawCentredString(A4[0] / 2, A4[1] - 150,
                              f"{dados_colaborador['usuario'].upper()} - {dados_colaborador['duracao_string']}")
        cnv.drawImage(grafico, -60, A4[1] - 530, width=A4[0] + 120, preserveAspectRatio=True)
        cnv.setFont("Helvetica", 12)

        tabela, tamanho_tabela = self.gerar_tabela_atividades(dados, TAMANHO_TABELA_ATIVIDADES_PP)
        tabela.wrapOn(cnv, 50, 50)
        tabela.drawOn(cnv, A4[0] - 550, A4[1] - 800)

        # Demais páginas
        if dados.shape[0] > TAMANHO_TABELA_ATIVIDADES_PP:
            indice_inicial = TAMANHO_TABELA_ATIVIDADES_PP
            while indice_inicial < dados.shape[0]:
                cnv.showPage()
                self.desenhar_layout_basico(cnv)
                tabela, tamanho_tabela = self.gerar_tabela_atividades(dados, TAMANHO_TABELA_FULL_PAGE, indice_inicial)
                tabela.wrapOn(cnv, 50, 50)

                tabela.drawOn(cnv, A4[0] - 550, A4[1] - self.calcular_offset_tabela(tamanho_tabela))
                indice_inicial += TAMANHO_TABELA_FULL_PAGE

        cnv.save()
        return 0

    @staticmethod
    def gerar_tabela_atividades(dados: pd.DataFrame, tamanho: int, indice_inicial: int = 0):
        data = [CABECALHO_ATIVIDADES]
        provisorio = dados.iloc[indice_inicial:(tamanho + indice_inicial), :]
        for index, row in provisorio.iterrows():
            data.append([Paragraph(row['descricao'][:60]), row['duracao_string']])
        tabela = Table(data, colWidths=[400, 100], rowHeights=20)
        style = [
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ]
        tabela.setStyle(style)

        return tabela, len(data)-1

    @staticmethod
    def desenhar_layout_basico(pagina: canvas.Canvas):
        pagina.drawImage('banner.png', 0, A4[1] - 90, width=A4[0], preserveAspectRatio=True)
        pagina.setFillColor(colors.grey)
        pagina.drawString(10, A4[1] - 830, 'B2ML Sistemas')
        pagina.setFillColor(colors.black)

    @staticmethod
    def calcular_offset_tabela(tamanho: int):
        return tamanho * 20 + 112

    @staticmethod
    def merge_pdf(nome: str, folder:str):
        pass
