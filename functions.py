#Definindo funçoes essencias para rodar APP

#importando libs
from datetime import datetime
from dateutil.parser import parse
import os
import pandas as pd
import time
import numpy as np
from PyPDF2 import PdfReader
from pathlib import Path
import re
from tkinter.filedialog import askdirectory

dataHoje = datetime.today()
hoje = dataHoje.strftime('%d-%m-%Y')
nome = 'Consolidado.csv'
start_time = time.time()

#pegar data de referecia
def DTref(data2:datetime):
   #criando lista
   listadata = []
   try:
      resp = parse(data2)
      print(resp)
      listadata.append(resp)
      #povoando a lista
      return listadata
   except ValueError:
            #setando erro
            raise ValueError("Formato incorreto, deve ser AAAA-MM-DD")


def buscaNomeArquivo(data:datetime):
   #pegando valores da main
   DataReferencia = DTref(data)
   #define serie
   lst=[]
   #determinando caminho de busca do arquivo
   print('Selecione a pasta de CONTRATOS SGF') 
   pasta = askdirectory(title='Selecione a pasta de CONTRATOS SGF')
   #pasta = r"C:\Users\cesargl\OneDrive - SERVICO DE APOIO AS MICRO E PEQUENAS EMPRESAS DE SAO PAULO - SEBRAE\Contratos"

   #for loop para povoar a lista com os endereços dos arquivos no caminho
   caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
   #for loop para pegar todos os arquivos no caminhos
   arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
   #separando apenas os .pdf
   pdfs = [arq for arq in arquivos if arq.lower().endswith(".pdf")]

   #separa os pdfs somente que são maiores ou igual a data de referência
   #seta duas tuplas "()" dentro de uma lista "[]"
   #primeira tupla separa a data de modificação do pdf e a segunda o nome do arquivo
   comparaDatas = [(datetime.strptime(time.ctime(os.path.getmtime(pdfs)),'%a %b %d %H:%M:%S %Y')\
                    for pdfs in pdfs if datetime.strptime(time.ctime(os.path.getmtime(pdfs)),\
                                                         '%a %b %d %H:%M:%S %Y') >= DataReferencia[0]),\
                     (os.path.basename(pdfs)\
                    for pdfs in pdfs if datetime.strptime(time.ctime(os.path.getmtime(pdfs)),\
                                                         '%a %b %d %H:%M:%S %Y') >= DataReferencia[0]),
                         (pdfs\
                    for pdfs in pdfs if datetime.strptime(time.ctime(os.path.getmtime(pdfs)),\
                                                         '%a %b %d %H:%M:%S %Y') >= DataReferencia[0])
                  
                                                         
                                                         ]
   
   #seta o dataframe e transpoe de linhas para colunas
   try:
      df = pd.DataFrame(comparaDatas).transpose()
   #renomeia as colunas
      df.columns = ['DATA','ARQUIVO','CAMINHO']
      return df
   finally:
   #printa o dataframe
      print(df)
       
      #loop para pegar todos os arquivos+caminho
      for nomesarquivos in  df['CAMINHO']:
          with open(nomesarquivos) as f: 
               pdf_file = open(f.name,'rb')
               dados_pdf = PdfReader(pdf_file)

               #define e faz contagem de caracteres dos objetos procurados
               numContrato = 'CONTRATO DE PRESTAÇÃO DE SERVIÇOS  Nº '
               contStrgContrato = len(numContrato)
               Sistema = 'SISTEMA'

               Unidade = 'Unidade/ER demandante: '
               contStrgUnidade = len(Unidade)

               GERENTE_LIMITE = '   Gerente'
                     
               cnpj = 'CNPJ/MF nº   '
               contStrgcnpj = len(cnpj)

               representante = 'Representante legal: '
               contStrgrepresentante = len(representante)
               RG_LIMITE = '  RG:'

               cpf = 'CPF:  '
               contStrgCPF = len(cpf)

               natureza = 'Natureza prestação de serviço (Consultoria ou Instrut oria):  '
               contStrgNatureza = len(natureza)

               objeto = 'Objeto da Contratação: '
               constStrgObjeto = len(objeto)

               valor = 'Valor:  '
               quebraValor = '('
               constStrValor = len(valor)

               vigencia = 'Vigência: '
               constStrVigencia = len(vigencia)

               cargaHoraria = 'Carga horária:  '
               constStrgCargaHoraria = len(cargaHoraria)

               Local = 'Local d e execução do serviço: '
               constStrgLocal = len(Local)

               Data_assinatura =  '***-'
               constStrgData_assinatura = len(Data_assinatura)+5

               nomeAssinatura = ' '
               constStrgnomeAssinatura = len(nomeAssinatura)

               assinaturafullInicio = ' '
               assinaturafullfim = 'Status:'
               assinaturaQuebra= ' - '

               #define paginas do documento para leitura
               
               ultimapagina= len(dados_pdf.pages)-1

               pagina1 = dados_pdf.pages[0]
               texto_da_pagina1 = pagina1.extract_text()
               texto_da_pagina1 = re.sub('\n','',texto_da_pagina1)

               pagina2 = dados_pdf.pages[1]
               texto_da_pagina2 = pagina2.extract_text() 
               texto_da_pagina2 = re.sub('\n','',texto_da_pagina2)   

               pagina_ultima = dados_pdf.pages[ultimapagina]
               texto_paginaUltima = pagina_ultima.extract_text()
               texto_paginaUltima = re.sub('\n','',texto_paginaUltima)   
               
               #unindo textos das paginas
               concatText = texto_da_pagina1+texto_da_pagina2


               #achando os valores no texto
               findContrato=concatText.find(numContrato)
               findSistema=concatText.find(Sistema)
               findUnidade=concatText.find(Unidade)
               findCnpj=concatText.find(cnpj,700)
               findRepresentante=concatText.find(representante)
               findcpf=concatText.find(cpf,1000)
               findnatureza=concatText.find(natureza)
               findObjeto=concatText.find(objeto)
               findValor=concatText.find(valor)
               findQuebraValor=concatText.find(quebraValor,findValor)
               findVigencia=concatText.find(vigencia)
               findcarga=concatText.find(cargaHoraria)
               findLocal=concatText.find(Local)
               findGERENTE=concatText.find(GERENTE_LIMITE)
               findRG=concatText.find(RG_LIMITE,1000)
               findData1 = texto_paginaUltima.find(Data_assinatura)
               findData2 = texto_paginaUltima.find(Data_assinatura,findData1+50)
               findData3 = texto_paginaUltima.find(Data_assinatura,findData2+50)
               findData4 = texto_paginaUltima.find(Data_assinatura,findData3+50)
               findNome1 = texto_paginaUltima.find(nomeAssinatura) 
               findNome2 = texto_paginaUltima.find(nomeAssinatura,findNome1+50)
               findNome3 = texto_paginaUltima.find(nomeAssinatura,findNome2+50)
               findNome4 = texto_paginaUltima.find(nomeAssinatura,findNome3+50)
               findAssinaturafull1 = texto_paginaUltima.find(assinaturafullInicio)
               findAssinaturafull2 = texto_paginaUltima.find(assinaturafullInicio,findAssinaturafull1+5)
               findAssinaturafull3 = texto_paginaUltima.find(assinaturafullInicio,findAssinaturafull2+5)
               findAssinaturafull4 = texto_paginaUltima.find(assinaturafullInicio,findAssinaturafull3+5)
               findAssinaturafull1_fim = texto_paginaUltima.find(assinaturafullfim)
               findAssinaturafull2_fim = texto_paginaUltima.find(assinaturafullfim,findAssinaturafull1_fim+5)
               findAssinaturafull3_fim = texto_paginaUltima.find(assinaturafullfim,findAssinaturafull2_fim+5)
               findAssinaturafull4_fim = texto_paginaUltima.find(assinaturafullfim,findAssinaturafull3_fim+5)
               findQuebra1 = texto_paginaUltima.find(assinaturaQuebra,findAssinaturafull1)
               findQuebra2 = texto_paginaUltima.find(assinaturaQuebra,findQuebra1+7)
               findQuebra3 = texto_paginaUltima.find(assinaturaQuebra,findAssinaturafull2)
               findQuebra4 = texto_paginaUltima.find(assinaturaQuebra,findQuebra3+7)
               findQuebra5 = texto_paginaUltima.find(assinaturaQuebra,findAssinaturafull3)
               findQuebra6 = texto_paginaUltima.find(assinaturaQuebra,findQuebra5+7)
               findQuebra7 = texto_paginaUltima.find(assinaturaQuebra,findAssinaturafull4)
               findQuebra8 = texto_paginaUltima.find(assinaturaQuebra,findQuebra7+7)
               
               #setando strings de assinatura
                     #setando datas das assinaturas
               if findAssinaturafull1 < 0:   
                     Assinatura1_split is None
               else:
                     Assinatura1_split = texto_paginaUltima[findAssinaturafull1+2:findQuebra1]

               if findAssinaturafull1 < 0 :   
                     DATA1_SPLIT is None
               else:
                     DATA1_SPLIT = texto_paginaUltima[findQuebra2+3:findQuebra2+22]
               ##
               if findAssinaturafull2 < 0 or findQuebra3 < 0:   
                     Assinatura2_split is None
               else:
                     Assinatura2_split = texto_paginaUltima[findAssinaturafull2+2:findQuebra3]

               if findAssinaturafull2 < 0 :   
                     DATA2_SPLIT is None
               else:
                     DATA2_SPLIT = texto_paginaUltima[findQuebra4+3:findQuebra4+22]
               ##
               if findAssinaturafull3 < 0:   
                     Assinatura3_split is None
               else:
                     Assinatura3_split = texto_paginaUltima[findAssinaturafull3+2:findQuebra5]

               if findAssinaturafull3 < 0:   
                     DATA3_SPLIT  is None
               else:
                     DATA3_SPLIT = texto_paginaUltima[findQuebra6+3:findQuebra6+22]
               
               ##
               if findAssinaturafull4 < 0:   
                     Assinatura4_split  is None
               else:
                     Assinatura4_split = texto_paginaUltima[findAssinaturafull4+2:findQuebra7]

               if findAssinaturafull4 < 0:   
                     DATA4_SPLIT is None
               else:
                     DATA4_SPLIT = texto_paginaUltima[findQuebra8+3:findQuebra8+22]


               #definindo dicionario dNomes, com unindo somentes os nomes e quando assinou
               NomeEDatas = { 'dNomes': [[Assinatura1_split,DATA1_SPLIT],
                                          [Assinatura2_split,DATA2_SPLIT],
                                          [Assinatura3_split,DATA3_SPLIT],
                                          [Assinatura4_split,DATA4_SPLIT]]}
               
               #setando dataframe de nomes e datas de assinaturas

               dfNomeDatas2 = pd.DataFrame(NomeEDatas)

               #separando dataframe em colunas distintas baseada na lista do dicionario dNomes
               dfNomeDatas2[['Assinatura','Data']] = pd.DataFrame(dfNomeDatas2.dNomes.to_list(),index=dfNomeDatas2.index)
               
               #dividindo colunas do dataframe
               dfNomeDatas3 = pd.DataFrame(dfNomeDatas2['dNomes'].to_list(), columns=['Assinatura','Data'])

               #convertendo datas em datetime
               dfNomeDatas3["Data"] = pd.to_datetime(dfNomeDatas3["Data"],dayfirst=True)

               #ordenando datas da mais recente para mais anterior
               dfNomeDataMaisRecente = dfNomeDatas3.sort_values(by='Data', ascending = False, inplace = False)     
               
               #ordenando datas da mais anterior para mais recente
               dfNomeDataMaisAnterior = dfNomeDatas3.sort_values(by='Data', ascending = True, inplace = False) 
               
               #criando base
               data_=[{}]
               compara_data=[]

               #criando dataframe  
               df2 = pd.DataFrame(data_)
               df3 = pd.DataFrame(compara_data)

               

               #definindo colunas
               df2["N° Contrato"] = concatText[findContrato+contStrgContrato:findSistema]
               df2["Unidade"] = concatText[findUnidade+contStrgUnidade:findGERENTE]
               df2["CNPJ"] = concatText[findCnpj+contStrgcnpj:findCnpj+contStrgcnpj+19]
               df2["Representante"] = concatText[findRepresentante+contStrgrepresentante:findRG]
               df2["CPF"] = concatText[findcpf+ contStrgCPF:findcpf+contStrgCPF+16]
               df2["Natureza prestação de serviço"] = concatText[findnatureza+contStrgNatureza:findnatureza+contStrgNatureza+12]
               df2["Objeto"] = concatText[findObjeto+constStrgObjeto:findObjeto+constStrgObjeto+232]
               df2["Valor"] = concatText[findValor+constStrValor:findQuebraValor]
               df2["Vigência"] = concatText[findVigencia+constStrVigencia:findVigencia+constStrVigencia+23]
               df2["Carga Horária"] = concatText[findcarga+constStrgCargaHoraria:findLocal]
               df2["Local de Execução"] = concatText[findLocal+constStrgLocal:findLocal+constStrgLocal+12]

               #setando nomes das assinaturas
               df2["assinatura1"] = texto_paginaUltima[findAssinaturafull1+2:findAssinaturafull1_fim]
               df2["assinatura2"] = texto_paginaUltima[findAssinaturafull2+2:findAssinaturafull2_fim]
               df2["assinatura3"] = texto_paginaUltima[findAssinaturafull3+2:findAssinaturafull3_fim]
               df2["assinatura4"] = texto_paginaUltima[findAssinaturafull4+2:findAssinaturafull4_fim]



               #setando datas das assinaturas
               if findData1 < 0:   
                     df2["DATA1"] = 0
               else:
                     df2["DATA1"] = texto_paginaUltima[findData1+constStrgData_assinatura:findData1+constStrgData_assinatura+20]

               if findData2 < findData1:   
                     df2["DATA2"] = 0
               else:
                     df2["DATA2"] = texto_paginaUltima[findData2+constStrgData_assinatura:findData2+constStrgData_assinatura+20]

               if findData3 < findData2:   
                     df2["DATA3"] = 0
               else:
                     df2["DATA3"] = texto_paginaUltima[findData3+constStrgData_assinatura:findData3+constStrgData_assinatura+20]  
               
               if findData4 < findData3:   
                     df2["DATA4"] = 0
               else:
                     df2["DATA4"] = texto_paginaUltima[findData4+constStrgData_assinatura:findData4+constStrgData_assinatura+20]


               #convertendo datas em datetime
               df3["DATA1"] = pd.to_datetime(df2["DATA1"],dayfirst=True)
               df3["DATA2"] = pd.to_datetime(df2["DATA2"],dayfirst=True) 
               df3["DATA3"] = pd.to_datetime(df2["DATA3"],dayfirst=True)
               df3["DATA4"] = pd.to_datetime(df2["DATA4"],dayfirst=True)

               #setando lista de datas
               compara_data=[df3['DATA1'].tolist(),df3['DATA2'].tolist(),df3['DATA3'].tolist(),df3['DATA4'].tolist()]

               
               #definindo a data mais recente
               df3["DATA_final"] = max(compara_data)

               #atribui valores a serie lst e atribui ao dataframe

               df2["ASSINATURA_SPLT1"] = Assinatura1_split
               df2["DATAASSINATURA_1"] = DATA1_SPLIT
               df2["ASSINATURA_SPLT2"] = Assinatura2_split
               df2["DATAASSINATURA_2"] = DATA2_SPLIT
               df2["ASSINATURA_SPLT3"] = Assinatura3_split
               df2["DATAASSINATURA_3"] = DATA3_SPLIT
               df2["ASSINATURA_SPLT4"] = Assinatura4_split
               df2["DATAASSINATURA_4"] = DATA4_SPLIT

               df2["DTMAISRECENTE"] = dfNomeDataMaisRecente['Data'].iloc[0]
               df2["ASSINAMAISRECENTE"] = dfNomeDataMaisRecente['Assinatura'].iloc[0]

               df2["DTMAISANTERIOR"] = dfNomeDataMaisAnterior['Data'].iloc[0]
               df2["ASSINAMAISANTERIOR"] = dfNomeDataMaisAnterior['Assinatura'].iloc[0]

               df2["nome_arquivo"] = nomesarquivos

               diretorio = Path(pasta)
               arquivo = diretorio/nomesarquivos
               tmpModificado = os.path.getmtime(arquivo)
               
               df2["DTMODIFICADO"] =  time.ctime(tmpModificado)
               df2["DTMODIFICADO"] = pd.to_datetime(df2["DTMODIFICADO"],dayfirst=True)
               lst.append(df2)
               
               print(nomesarquivos)
               #uni as dfs 
               df2 = pd.concat(lst, axis=0 )
               df2.to_csv(f'{hoje}-{nome}', index = False)
          
      print("--- %s seconds ---" % (time.time() - start_time))   
