#importando libs

from pandas import DataFrame
from PyPDF2 import PdfReader
from datetime import datetime

#importando funcoes
from functions import DTref, buscaNomeArquivo

#Definir input de data
x = input('Qual a data de referencia? (ex:2024-12-01) ')


#Inicio da Main
def main():
 #atribuindo data dentro da main
 if x is not None:
    try:
        #atribuindo data dentro da funcao
        buscaNomeArquivo(x)
    #except Exception as e:
         #print("erro")
    finally:
        print('FINALIZADO') 

#Fim da main
if __name__ == "__main__":
      main()    