# splitPDF

splitPDF é um programa que divide arquivos pdf.

É possível escolher entre dividir apenas um arquivo de entrada ou todos os arquivos de um determinado diretório.

É possível escolher entre dividir o(s) arquivo(s) de entrada em uma determinada quantidade de partes, ou limitar o tamanho máximo dos arquivos de saída.

Para rodar a versão GUI: (i) baixar e executar o executável windows ou (ii)baixar os quatro arquivos .py e executar "python3 pdf_gui.py"

![gui](/imagens/imgui.jpg)

Para rodar a versão CLI: é possível baixar apenas splitpdf.py, mensagens.py e erros.py.

- Uso: python3 splitpdf.py entrada pasta modo
  - entrada: número inteiro maior que zero para o tamanho máximo ou quantidade de partes.
  - pasta: arquivo .pdf ou diretório onde estão os arquivos para dividir.
  - modo: tamanho ou partes
