from pathlib import Path
import pyinputplus as pyip
import math, PyPDF2, os


def executa(paginas_p_arquivo, pdf_reader, contador_paginas, nome, parte, tamanho_maximo, pasta_doc):
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

    str_nome = f'{nome[:-4]} - parte{parte}.pdf'
    end_destino = pasta_doc / str_nome

    pdf_file_out = open(end_destino, 'wb')
    pdf_writer.write(pdf_file_out)
    pdf_file_out.close()

    if os.stat(pdf_file_out.name).st_size > tamanho_maximo:
        #paginas_p_arquivo -= 1
        paginas_p_arquivo = math.floor(paginas_p_arquivo - 0.05 * paginas_p_arquivo)
        contador_paginas = executa(paginas_p_arquivo, pdf_reader, contador_orig, nome, parte, tamanho_maximo, pasta_doc)

    return contador_paginas


def divide_pdf(pasta_arquivos, arquivo, tamanho_maximo, pasta_doc):
    pdf_file_in = open(pasta_arquivos / arquivo, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_in)

    tamanho_maximo *= 1000 * 1000
    tamanho_entrada = os.stat(pdf_file_in.name).st_size

    paginas_p_arquivo = tamanho_maximo // (tamanho_entrada // pdf_reader.numPages) - 1
    contador_paginas = 0

    parte = 1
    while contador_paginas >= 0:
        contador_paginas = executa(paginas_p_arquivo, pdf_reader, contador_paginas, arquivo, parte, tamanho_maximo, pasta_doc)
        parte += 1

    pdf_file_in.close()


def control(tam, dir):
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
            sub_pasta = arquivo[:-4]
            pasta_doc = pasta_arquivos / sub_pasta
            Path(pasta_doc).mkdir()
            divide_pdf(pasta_arquivos, arquivo, tam, pasta_doc)


def main():
    control()

if __name__ == "__main__":
    main()
