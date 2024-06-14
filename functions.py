#Definindo funçoes essencias para rodar APP

#importando libs
from datetime import datetime

from dateutil.parser import parse

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
   print("buscarArquivosPrint")