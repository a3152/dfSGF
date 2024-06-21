#importando libs

from pandas import DataFrame
from PyPDF2 import PdfReader
from datetime import datetime

#importando funcoes
from functions import buscaNomeArquivo

#Definir input de data

x = input('Qual a data de partida (menor ou igual a  '  + datetime.now().strftime("%Y/%m/%d") + ')? (insira no formato AAAA-MM-DD ex:2024-01-01) ')


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
        input("Pressione <enter> para encerrar!") 

#Fim da main
if __name__ == "__main__":
      main()    