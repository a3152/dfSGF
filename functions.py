#Definindo funçoes essencias para rodar APP

#importando libs
from datetime import datetime
from dateutil.parser import parse
import os
import pandas as pd
import time
import numpy as np

#pegar data de referecia
def DTref(data2:datetime):
   listadata = []
   try:
      resp = parse(data2)
      print(resp)
      listadata.append(resp)
      return listadata
   except ValueError:
            raise ValueError("Formato incorreto, deve ser AAAA-MM-DD")


def buscaNomeArquivo(data:datetime):
   DataReferencia = DTref(data)
   pasta = r"C:\Users\cesargl\OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE\Contratos"

   caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
   arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
   pdfs = [arq for arq in arquivos if arq.lower().endswith(".pdf")]
   comparaDatas = [(datetime.strptime(time.ctime(os.path.getmtime(arq)),'%a %b %d %H:%M:%S %Y')\
                    for arq in pdfs if datetime.strptime(time.ctime(os.path.getmtime(arq)),\
                                                         '%a %b %d %H:%M:%S %Y') <= DataReferencia[0]),\
                     (os.path.basename(arq)\
                    for arq in pdfs if datetime.strptime(time.ctime(os.path.getmtime(arq)),\
                                                         '%a %b %d %H:%M:%S %Y') <= DataReferencia[0])]
   

   df = pd.DataFrame(comparaDatas).transpose()
   df.columns = ['DATA','ARQUIVO']

   print(df)
   

