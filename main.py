#importando libs

from pandas import DataFrame
from PyPDF2 import PdfReader
from datetime import datetime

#importando arquivos
from functions import DTref, buscaNomeArquivo

x = input('Qual a data de referencia? (ex:2024-12-01) ')
#definindo caminho para busca de arquivos
#caminho = "C:/Users/cesargl/OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE/.git/scriptsSebrae_/teste_arquivos"
caminho = r"C:\Users\cesargl\OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE\Contratos"

def main():
 if x is not None:
    try:
        buscaNomeArquivo(x)
    except Exception as e:
         print("erro") 

if __name__ == "__main__":
      main()    