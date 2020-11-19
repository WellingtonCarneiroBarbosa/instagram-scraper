#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
# Instagram Scraper Comments
# Developed by Wellington Barbosa
# At May, 07 - 2020 
# Follow me on github https://github.com/wellingtoncarneirobarbosa
# --------------------------------------------------------------------
from datetime import datetime
import time, sys, platform, os, random, csv

import pandas as pd

# -----
# api 
# -----
from igramscraper.instagram import Instagram

class instagramScraper:
    def __init__(self, sleep_between_requests=0):
        executionOn = platform.system()
        print("\n")
        print("\r[!] Executando o bot em sistema " + str(executionOn) )
        print("\r[!] Iniciado em => " + str(datetime.now().strftime("%d/%m/%Y")) + " as " + str(datetime.now().strftime("%H:%M")) )
        self.start = datetime.now()

    def getLen(numero):
        numero = abs(int(numero))
        if numero < 2:
            return 1
        count = 0
        valor = 1
        while valor <= numero:
            valor *= 10
            count += 1
        return count

    def excel_exporter(self, codes, filename):
            try:
                temp = {}                    
                temp_codes = []
                temp_names = []
                temp_comments = []
                if os.path.isfile(filename):
                    saved = pd.read_csv(filename)
                    temp_names.extend(saved['a - username'])
                    temp_comments.extend(saved['b - comment'])
                temp_codes.extend(codes)
                temp.update({'a - username': temp_names, 'b - comment': temp_comments, 'c - codes': temp_codes})
                df = pd.DataFrame(temp)
                df.to_csv(filename, index=False, encoding='utf-8')
            except Exception as e:
                print("\rErro no codigo do excel_exporter")
                print("\rComunique o desenvolvedor")
                print("\rCodigo do erro (mostre isso ao desenvolvedor) => ")
                print(e)

    def getPost(self):
        # ------------------
        # post credencials
        # ------------------
        while True:
            try:
                print( "\n------------------------------------------------------\n" )
                self.postCode = str(input("\r[!] Insira o ID da publicacao => "))
            except:
                print(  "\n------------------------------------------------------\n" )
                print(  "\r[!] Ops...\nEsse id e invalido" )
                print(  "\n------------------------------------------------------\n" )
                continue
            break
        print( "\n------------------------------------------------------\n" )
        self.qtdComments = int(input("\r[!] Insira a quantidade de comentarios que deseja extrair: "))
        print( "\n------------------------------------------------------\n" )
        self.generateCodes = str(input("\r[!] Deseja que sejam gerados os numeros da sorte no final da extracao?\n[s] ou [n] => "))
        while (str(self.generateCodes) != str("s") and str(self.generateCodes)  != str("n")):
            print(  "\n------------------------------------------------------\n" )
            print(  "\r[!] Ops... Digite [s] para sim ou [n] para nao ")
            print(  "\n------------------------------------------------------\n" )
            self.generateCodes = str(input("\r[!] Deseja que sejam gerados os numeros da sorte no final da extracao?\n[s] ou [n] => "))
        print( "\n------------------------------------------------------\n" )
        if(self.generateCodes == "s"):
            self.algarismCodes = int(input("\r[!] Insira a quantidade de algarismos que o codigo de cada comentario deve possuir\nDeve ser maior ou igual a " + str(instagramScraper.getLen(self.qtdComments)) + " => ") )
            while self.algarismCodes < instagramScraper.getLen(self.qtdComments):
                print(  "\n------------------------------------------------------\n" )
                print(  "\r[!] Ops... ")
                print(  "\n------------------------------------------------------\n" )
                self.algarismCodes = int(input("\r[!] Insira a quantidade de algarismos que o codigo de cada comentario deve possuir\nDeve ser maior que " + str(instagramScraper.getLen(self.qtdComments)) + " => ") )


    # ------------------
    # start scrapper
    # -----------------
    def scraper(self):
        # get api
        instagram = Instagram()
        try:
            print("\r[!] Realize o login para prosseguir. Pode ser que o instagram bloqueie o login")
            print("\r[!] Caso ocorra o bloqueio, entre em seu instagram atraves do celular e aperte o botao 'fui eu'")
            login = str(input("\r[!] Insira seu username => "))
            password = str(input("\r[!] Insira sua senha => "))
            print("\r[!] Tentando realizar login")
            # authentication supported
            instagram.with_credentials(login, password)
            instagram.login()
            logged = True
        except:
            logged = False
            print("Login e/ou senha incorreto(s) | Ou login bloqueado!! Por favor, reinicie o programa e tente novamente")
        if logged:
            print("\r[!] Logado")

        # ---------------
        # try get post
        # ---------------
        try:
            instagramScraper.getPost(self)
            startExtractCommentsTime = datetime.now()
            print("\n------------------------------------------------------\n"             )
            print("\r[!] Carregando comentarios... isso pode levar horas"      )
            print("\n------------------------------------------------------\n"             )

            # -------------------
            # conter for codes
            # -------------------
            if(self.generateCodes == "s"):
                n = self.algarismCodes
                initialConter = ""
                endConter = ""

                for l in range(n):
                    l += 1
                    if(l == 1):
                        initialConter += str(1)
                    else:
                        initialConter += str(0)
                    endConter += str(9)

            comments = instagram.get_media_comments_by_id(self.postCode, self.qtdComments)
        except Exception as e:
            print("Um erro inesperado ocorreu :( reporte-o ao desenvolvedor \n \n")
            print(e)
            pass

        if(self.generateCodes == "s"):
            try:
                startGenerateCodesTime = datetime.now()

                #count how many comments was getted
                with open(comments['csv_file'],"r") as f:
                    reader = csv.reader(f,delimiter = ",")
                    data = list(reader)
                    comments_qtd = len(data)

                print("\n------------------------------------------------------\n")
                print("\r[!] Gerando codigo para " + str(comments['comments']) + " comentarios")

                codes = random.sample(range(int(initialConter), int(endConter)), int(comments_qtd))
                endGenerateCodesTime = datetime.now() 
                print("\r[!] Codigos gerados com sucesso!")
                

                startSavingCodesTime = datetime.now()
                print("\r[!] Salvando codigos no arquivo " + str(comments['csv_file']))
                codes.pop(0)
                self.excel_exporter(codes, comments['csv_file'])
                print("\r[!] Codigos salvos com sucesso!")
                endSavingCodesTime = datetime.now()

            except Exception as e:
                print("\r[x] Erro ao gerar e/ou salvar codigos. Os comentarios foram salvos normalmente.")
                print("\n")
                print("\r[!] Por favor, envie o erro abaixo ao desenvolvedor")
                print("\n")
                print(str(e))
                pass

        # -----------
        # show logs
        # -----------
        
        end = datetime.now().strftime("%d/%m/%Y %H:%M")
        endExecution = datetime.now()
        executionTime =  endExecution - self.start
        if(self.generateCodes == "s"):
            endGenerateCodes = endGenerateCodesTime - startGenerateCodesTime
            endSavingCodes = endSavingCodesTime - startSavingCodesTime
        print("\n------------------------------------------------------\n"                   )
        print("\r[!] LOGS\n"                                                                 )
        print("\r[!] Comentarios obtidos e salvos => "     + str(comments['comments'])                )
        print("\r[!] Deveriam ser obtidos => "    + str(self.qtdComments)                    )
        if(self.generateCodes == "s"):
            print("\r[!] Tempo de geracao de codigos => " + str(endGenerateCodes))
            print("\r[!] Tempo para salvar os codigos => " + str(endSavingCodes))
        print("\r[!] Inicio => "      + str(self.start.strftime("%d/%m/%Y %H:%M"))           )
        print("\r[!] Termino => "     + str(end)                                             )
        print("\r[!] Tempo total de execucao => " + str(executionTime)                       )
        print("\r[!] Resultado disponivel em => " + str(comments['csv_file']))
        print( "\n------------------------------------------------------\n"                  )
        input("Pressione qualquer tecla para encerrar")
# -------------------
# start bot
# -------------------
bot = instagramScraper()
bot.scraper()