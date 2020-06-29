import os

from Pdf import PdfSize, PdfParts
from Errors import TooFewPagesError, EmptyFileError
from input_sanitizer import sanitize_input
from mensagens import PASTA_JA_EXISTE, TOO_FEW_PAGES, EMPTY_FILE


def get_pdf_instance(mode, pdf_args):
    sop, f, outpath = pdf_args
    if mode == "tamanho":
        return PdfSize(sop, f, outpath)
    else:
        try:
            p = PdfParts(sop, f, outpath)
        except TooFewPagesError:
            print(TOO_FEW_PAGES)
            raise TooFewPagesError
        return p


def create_outfolder(outpath):
    try:
        os.mkdir(outpath)
    except FileExistsError:
        print(PASTA_JA_EXISTE)
        raise FileExistsError


def split_pdf(pdf_args, outpath):
    sop, filepath, mode = pdf_args
    with open(filepath, "rb") as f:
        p = get_pdf_instance(mode, (sop, f, outpath))
        try:
            p.split()
        except EmptyFileError:
            print(EMPTY_FILE)
            raise EmptyFileError


def list_selected_files(path):
    if path.endswith(".pdf"):
        return [path]
    else:
        return [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".pdf")]


def split_infiles(sop, path, mode):
    for filepath in list_selected_files(path):
        outpath = os.path.join(str(filepath)[:-4])
        create_outfolder(outpath)
        split_pdf((sop, filepath, mode), outpath)


def main():
    sop, path, mode = sanitize_input()
    split_infiles(sop, path, mode)


if __name__ == "__main__":
    main()
