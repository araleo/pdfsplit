class TooFewPagesError(Exception):
    # levantada quando o arquivo pdf tem menos paginas que a quantidade de partes que se deseja dividir
    pass

class EmptyFileError(Exception):
    # levantada quando um arquivo é dividido por tamanho até não sobrar nenhuma pagina
    # normalmente quando uma das paginas é maior que o tamanho máximo
    pass
