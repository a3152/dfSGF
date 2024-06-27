import pandas as pd
import time
from PyPDF2 import PdfReader
from tkinter.filedialog import askdirectory
from datetime import datetime
from dateutil.parser import parse
import os

# Configurações iniciais
dataHoje = datetime.today()
hoje = dataHoje.strftime('%d-%m-%Y')
nome = 'Consolidado.csv'
start_time = time.time()

class PDFProcessor:
    def __init__(self, data_ref):
        self.data_ref = self.parse_date(data_ref)
        self.contratos = []

    def parse_date(self, date_str):
        try:
            return parse(date_str)
        except ValueError:
            raise ValueError("Formato incorreto, deve ser AAAA-MM-DD")

    def buscar_arquivos(self):
        print('Selecione a pasta de CONTRATOS SGF')
        pasta = askdirectory(title='Selecione a pasta de CONTRATOS SGF')
        caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        return [arq for arq in arquivos if arq.lower().endswith(".pdf")]

    def processar_arquivos(self, arquivos):
        for arquivo in arquivos:
            print(f"Processando arquivo: {arquivo}")  # Adicionado para debug
            if datetime.strptime(time.ctime(os.path.getmtime(arquivo)), '%a %b %d %H:%M:%S %Y') >= self.data_ref:
                self.processar_pdf(arquivo)
        self.salvar_dados()

    def processar_pdf(self, caminho_pdf):
        try:
            pdf_file = open(caminho_pdf, 'rb')
            dados_pdf = PdfReader(pdf_file)

            textos_paginas = [page.extract_text().replace('\n', '') for page in dados_pdf.pages[:2]]
            texto_completo = ''.join(textos_paginas)
            texto_ultima_pagina = dados_pdf.pages[-1].extract_text().replace('\n', '')

            dados_contrato = {
                "N° Contrato": self.extrair_texto(texto_completo, 'CONTRATO DE PRESTAÇÃO DE SERVIÇOS  Nº ', 'SISTEMA'),
                "Unidade": self.extrair_texto(texto_completo, 'Unidade/ER demandante: ', '   Gerente'),
                "CNPJ": self.extrair_texto(texto_completo, 'CNPJ/MF nº   ', 19),
                "Representante": self.extrair_texto(texto_completo, 'Representante legal: ', '  RG:'),
                "CPF": self.extrair_texto(texto_completo, 'CPF:  ', 16),
                "Natureza prestação de serviço": self.extrair_texto(texto_completo, 'Natureza prestação de serviço (Consultoria ou Instrut oria):  ', 12),
                "Objeto": self.extrair_texto(texto_completo, 'Objeto da Contratação: ', 232),
                "Valor": self.extrair_texto(texto_completo, 'Valor:  ', '('),
                "Vigência": self.extrair_texto(texto_completo, 'Vigência: ', 23),
                "Carga Horária": self.extrair_texto(texto_completo, 'Carga horária:  ', 'Local d e execução do serviço: '),
                "Local de Execução": self.extrair_texto(texto_completo, 'Local d e execução do serviço: ', 12),
                "nome_arquivo": caminho_pdf,
                "DTMODIFICADO": self.converter_data_modificacao(caminho_pdf)
            }

            self.processar_assinaturas(texto_ultima_pagina, dados_contrato)
            self.contratos.append(dados_contrato)
        except Exception as e:
            print(f"Erro ao processar o arquivo {caminho_pdf}: {e}")

    def extrair_texto(self, texto, inicio, fim):
        try:
            if isinstance(fim, int):
                return texto[texto.find(inicio) + len(inicio):texto.find(inicio) + len(inicio) + fim]
            return texto[texto.find(inicio) + len(inicio):texto.find(fim)]
        except:
            return None

    def processar_assinaturas(self, texto, dados_contrato):
        signature_keys = [
            ('assinatura1', 'DATA1', ' ', 'Status:', ' - '),
            ('assinatura2', 'DATA2', ' ', 'Status:', ' - '),
            ('assinatura3', 'DATA3', ' ', 'Status:', ' - '),
            ('assinatura4', 'DATA4', ' ', 'Status:', ' - ')
        ]

        for key, data_key, start, end, split in signature_keys:
            start_idx = texto.find(start)
            end_idx = texto.find(end, start_idx)
            split_idx = texto.find(split, start_idx)
            dados_contrato[key] = texto[start_idx + len(start):split_idx].strip() if start_idx != -1 else None
            dados_contrato[data_key] = texto[split_idx + len(split):end_idx].strip() if split_idx != -1 else None

        df_assinaturas = pd.DataFrame([{'Assinatura': dados_contrato[key], 'Data': dados_contrato[data_key]} for key, data_key, *_ in signature_keys])

        try:
            # Especifica o formato das datas se possível
            df_assinaturas['Data'] = pd.to_datetime(df_assinaturas['Data'], format='%d/%m/%Y', errors='coerce')
        except ValueError:
            df_assinaturas['Data'] = pd.to_datetime(df_assinaturas['Data'], errors='coerce')

        df_assinaturas = df_assinaturas.dropna().sort_values(by='Data')

        if not df_assinaturas.empty:
            dados_contrato["DTMAISRECENTE"] = df_assinaturas.iloc[-1]['Data']
            dados_contrato["ASSINAMAISRECENTE"] = df_assinaturas.iloc[-1]['Assinatura']
            dados_contrato["DTMAISANTERIOR"] = df_assinaturas.iloc[0]['Data']
            dados_contrato["ASSINAMAISANTERIOR"] = df_assinaturas.iloc[0]['Assinatura']

    def converter_data_modificacao(self, arquivo):
        return pd.to_datetime(time.ctime(os.path.getmtime(arquivo)), dayfirst=True)

    def salvar_dados(self):
        df_final = pd.DataFrame(self.contratos)
        df_final.to_csv(f'{hoje}-{nome}', index=False)
        print("--- %s seconds ---" % (time.time() - start_time))

# Função principal
def main():
    data_ref = input(f'Qual a data de partida (menor ou igual a {datetime.now().strftime("%Y/%m/%d")})? (insira no formato AAAA-MM-DD ex:2024-01-01) ')
    if data_ref:
        processor = PDFProcessor(data_ref)
        arquivos = processor.buscar_arquivos()
        processor.processar_arquivos(arquivos)
        print('Processamento finalizado.')
        input("Pressione <enter> para encerrar!")

if __name__ == "__main__":
    main()
