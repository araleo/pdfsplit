import math
import os
import sys

import pyinputplus as pyip
import PyPDF2
from pathlib import Path

from errors import EmptyFileError, TooFewPagesError
from mensagens import *


def verifica_pasta_vazia(pasta):
    arquivos = os.listdir(pasta)
    if not arquivos:
        os.rmdir(pasta)


def verifica_arquivo_vazio(arq):
    with open(arq, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        if reader.numPages == 0:
            f.close()
            os.remove(arq)
            raise EmptyFileError


def executa_por_tamanho(paginas_p_arquivo, pdf_reader, contador_paginas, nome, parte, tamanho_maximo, pasta_doc):
    pdf_writer = PyPDF2.PdfFileWriter()
    contador_orig = contador_paginas

    for pagina in range(paginas_p_arquivo):
        try:
            page_obj = pdf_reader.getPage(contador_paginas)
            pdf_writer.addPage(page_obj)
            contador_paginas += 1
        except IndexError:
            contador_paginas = -1
            break

    end_destino = pasta_doc / f'{nome[:-4]} - parte{parte}.pdf'
    pdf_file_out = open(end_destino, 'wb')
    pdf_writer.removeLinks()
    pdf_writer.write(pdf_file_out)
    pdf_file_out.close()
    verifica_arquivo_vazio(end_destino)

    if os.stat(pdf_file_out.name).st_size > tamanho_maximo:
        paginas_p_arquivo = math.floor(paginas_p_arquivo * 0.95)
        contador_paginas = executa_por_tamanho(
            paginas_p_arquivo,
            pdf_reader,
            contador_orig,
            nome,
            parte,
            tamanho_maximo,
            pasta_doc
        )

    return contador_paginas


def divide_por_tamanho(pasta_arquivos, arquivo, tamanho_maximo, pasta_doc):
    with open(pasta_arquivos / arquivo, 'rb') as pdf_file_in:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_in)

        tamanho_maximo *= 1000 * 1000
        tam_pagina = os.stat(pdf_file_in.name).st_size // pdf_reader.numPages
        paginas_p_arquivo = tamanho_maximo // tam_pagina - 1
        contador_paginas = 0

        parte = 1
        while contador_paginas >= 0:
            contador_paginas = executa_por_tamanho(
                paginas_p_arquivo,
                pdf_reader,
                contador_paginas,
                arquivo,
                parte,
                tamanho_maximo,
                pasta_doc
            )
            parte += 1


def divide_em_partes(pasta_arquivos, arquivo, numero_partes, pasta_doc):
    pdf_file_in = open(pasta_arquivos / arquivo, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_in)

    if pdf_reader.numPages < numero_partes:
        raise TooFewPagesError

    paginas_p_arquivo = pdf_reader.numPages // numero_partes
    resto_paginas = pdf_reader.numPages % numero_partes
    contador_paginas = 0

    for parte in range(numero_partes):
        pdf_writer = PyPDF2.PdfFileWriter()
        for x in range(paginas_p_arquivo):
            page_obj = pdf_reader.getPage(contador_paginas)
            pdf_writer.addPage(page_obj)
            contador_paginas += 1

        if parte == numero_partes - 1:
            for x in range(resto_paginas):
                page_obj = pdf_reader.getPage(contador_paginas)
                pdf_writer.addPage(page_obj)
                contador_paginas += 1

        end_destino = pasta_doc / f'{arquivo[:-4]} - parte{parte+1}.pdf'
        pdf_file_out = open(end_destino, 'wb')
        pdf_writer.removeLinks()
        pdf_writer.write(pdf_file_out)
        pdf_file_out.close()


def control(entrada, dir, modo):
    pasta_arquivos = ''
    lista_arquivos = []

    if dir[-4:] == '.pdf':
        pos = dir.rfind('/')
        if pos < 0:
            pos = dir.rfind('\\')
        pasta_arquivos = Path(os.path.abspath(dir[:pos]))
        lista_arquivos.append(dir[pos+1:])
    else:
        pasta_arquivos = Path(os.path.abspath(dir))
        lista_arquivos = os.listdir(pasta_arquivos)

    for arquivo in lista_arquivos:
        if arquivo.endswith('.pdf'):
            pasta_doc = pasta_arquivos / arquivo[:-4]
            Path(pasta_doc).mkdir()

            if modo == 'tamanho':
                try:
                    divide_por_tamanho(
                        pasta_arquivos,
                        arquivo,
                        entrada,
                        pasta_doc
                    )
                except EmptyFileError:
                    print(EMPTY_FILE)
                    verifica_pasta_vazia(pasta_doc)
                    return 1
            elif modo == 'partes':
                try:
                    divide_em_partes(
                        pasta_arquivos,
                        arquivo,
                        entrada,
                        pasta_doc
                    )
                except TooFewPagesError:
                    print(TOO_FEW_PAGES)
                    verifica_pasta_vazia(pasta_doc)
                    return 2

            verifica_pasta_vazia(pasta_doc)
    return 0


def main():
    # verifica a quantidade de argumentos
    if len(sys.argv) != 4:
        print(TEXTO_ARGV)
        exit()

    # converte o primeiro argumento para tipo inteiro
    # e verifica se é maior que zero
    try:
        entrada = int(sys.argv[1])
    except ValueError:
        print(TEXTO_ARGV)
        exit()
    else:
        if entrada <= 0:
            print(TEXTO_ARGV)
            exit()

    # verifica se o segundo argumento é um diretório
    # ou arquivo pdf válido
    caminho = sys.argv[2]
    if not os.path.exists(Path(os.path.abspath(caminho))):
        print(TEXTO_ARGV)
        exit()

    # verifica o terceiro argumento
    modo = sys.argv[3]
    if modo != "tamanho" and modo != "partes":
        print(TEXTO_ARGV)
        exit()

    try:
        control(entrada, caminho, modo)
    except FileExistsError:
        print(PASTA_JA_EXISTE)


if __name__ == "__main__":
    main()
