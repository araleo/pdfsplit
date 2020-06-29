import os

import PyPDF2

from Errors import TooFewPagesError, EmptyFileError


class Pdf:
    def __init__(self, file, outpath):
        self.reader = PyPDF2.PdfFileReader(file)
        self.pages = self.reader.pages
        self.outpath = outpath
        self.nome = f"teste"

    def write_outfile(self, writer, name):
        with open(os.path.join(self.outpath, name), "wb") as f:
            writer.removeLinks()
            writer.write(f)
            writer = PyPDF2.PdfFileWriter()
        return writer


class PdfSize(Pdf):
    def __init__(self, max_size, file, outpath):
        super().__init__(file, outpath)
        self.max_size = max_size * 1000 * 1000
        self.page_size = os.stat(file.name).st_size // self.reader.numPages
        self.pages_file = self.max_size // self.page_size - 1
        self.pages_written = 0
        self.counter = 0

    def split(self):
        part = 1
        while True:
            current_pages = self.pages_file
            name = f"teste{part}.pdf"
            self.create_file(name)
            filepath = os.path.join(self.outpath, name)
            while not self.check_size(filepath):
                current_pages -= 1
                self.recreate_file(current_pages, name, filepath)
            self.pages_written = 0
            part += 1

            if self.counter >= len(self.pages) - 1:
                break

    def check_size(self, filepath):
        with open(filepath, "rb") as f:
            size = os.stat(f.name).st_size
        return size <= self.max_size

    def add_page(self, writer):
        try:
            writer.addPage(self.pages[self.counter])
        except IndexError:
            pass
        else:
            self.pages_written += 1
            self.counter += 1
        return writer

    def create_file(self, name, pages=None):
        writer = PyPDF2.PdfFileWriter()
        pages = self.pages_file if pages is None else pages
        for _ in range(pages):
            writer = self.add_page(writer)
            if self.counter >= len(self.pages):
                break
        self.write_outfile(writer, name)
        self.verify_empty_file(os.path.join(self.outpath, name))

    def recreate_file(self, pages, name, filepath):
        os.remove(filepath)
        self.counter -= self.pages_written
        self.pages_written = 0
        self.create_file(name, pages)

    def verify_empty_file(self, filepath):
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfFileReader(f)
            if reader.numPages == 0:
                f.close()
                os.remove(filepath)
                raise EmptyFileError


class PdfParts(Pdf):
    def __init__(self, num_parts, file, outpath):
        super().__init__(file, outpath)
        self.num_parts = num_parts
        self.pages_file, self.rest_pages = divmod(self.reader.numPages, self.num_parts)
        self.check_for_min_pages()

    def split(self):
        writer = PyPDF2.PdfFileWriter()
        for num, page in enumerate(self.pages):
            writer.addPage(page)
            if self.check_for_write(num):
                writer = self.write_outfile(writer, f"teste{self.set_part(num)}.pdf")

    def check_for_write(self, num):
        if num == len(self.pages) - 1:
            return True
        end_of_part_check = num % self.pages_file == self.pages_file - 1
        end_of_file_check = not num == (self.pages_file * self.num_parts) - 1
        return end_of_part_check and end_of_file_check

    def set_part(self, num):
        part = num // self.pages_file
        return part + 1 if part < self.num_parts else self.num_parts

    def check_for_min_pages(self):
        if len(self.pages) < self.num_parts:
            raise TooFewPagesError
