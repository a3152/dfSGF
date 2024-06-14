#importando libs

from pandas import DataFrame
from PyPDF2 import PdfReader

#importando arquivos
from functions import DTref

#definindo caminho para busca de arquivos

x = 1
#caminho = "C:/Users/cesargl/OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE/.git/scriptsSebrae_/teste_arquivos"
caminho = r"C:\Users\cesargl\OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE\Contratos"

def main():
 if x is not None:
    try:
        DTref()
    except Exception as e:
         print("erro") 

if __name__ == "__main__":
      main()    