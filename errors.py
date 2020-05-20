class TooFewPagesError(Exception):
    """
    Exceção levantada quando o arquivo pdf tem menos paginas que
    a quantidade de partes que se deseja dividir.
    """
    pass

class EmptyFileError(Exception):
    """
    Exceção levantada quando um arquivo é dividido por tamanho até
    não sobrar nenhum página. Normalmente quando o tamanho de
    uma das páginas é maior que o tamanho máximo permitido por parte.
    """
    pass
