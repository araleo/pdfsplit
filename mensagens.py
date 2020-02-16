TEXTO_INFO = """
Olá, obrigado por usar o splitPDF!

Com ele você pode dividir seus arquivos .pdf.

Primeiro escolha se deseja dividir o arquivo por tamanho ou por partes.

A divisão por tamanho produzirá diversos arquivos de saída com o tamanho máximo que você determinar.

A divisão por partes dividirá o arquivo em quantas partes você escolher.

Para dividir todos os arquivos .pdf que estão em uma pasta do seu computador, pressione o botão "Escolher pasta".
Uma janela irá se abrir. Navegue até a pasta em que estão os arquivos .pdf que deseja dividir e aperte ok.

Para dividir apenas um arquivo .pdf, pressione o botão "Escolher arquivo" e, na janela que abrir, procure o arquivo em seu computador.

Após selecionar a pasta ou arquivo, o seu endereço deverá aparecer na barra abaixo do botão "Dividir".
Confirme se selecionou a pasta ou arquivo correto.

Digite o tamanho máximo que os arquivos de saída poderão ter, ou a quantidade de partes que deseja.
Somente são aceitos números inteiros.
Se você digitar algo que não seja um número, uma mensagem de erro irá aparecer.
Mas, se digitar um número real, ele será automaticamente convertido para o inteiro anterior.

Clique no botão "Dividir" e aguarde até que a mensagem "Sucesso" apareça na barra abaixo do botão.

https://github.com/araleo/pdfsplit
"""


TEXTO_ARGV = """
Uso: python3 splitpdf.py entrada pasta modo
entrada: número inteiro maior que zero para o tamanho máximo ou quantidade de partes.
pasta: arquivo .pdf ou diretório onde estão os arquivos para dividir.
modo: tamanho ou partes
"""


TOO_FEW_PAGES = """
Impossível dividir um dos arquivos. Parece que ele possui menos páginas que o número de partes.
"""

EMPTY_FILE = """
Impossível dividir um dos arquivos. Parece que uma das páginas é maior que o tamanho máximo especificado.
"""

PASTA_JA_EXISTE = """
Já existe uma pasta com o nome de algum dos arquivos. Por favor renomeie a pasta ou o arquivo.
"""
