from errors import EmptyFileError, TooFewPagesError
from mensagens import *
from splitpdf import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class Pdf(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = LabelFrame(text="Divisor de PDFs", padx=50, pady=50)
        self.frame.pack()
        self.funcao_divisao = 'tamanho'
        r = StringVar()
        
        self.radio_tam = Radiobutton(self.frame, text="Dividir por tamanho", variable=r, value="tamanho", command=lambda: self.define_funcao(r.get()))
        self.radio_partes = Radiobutton(self.frame, text="Dividir por partes", variable=r, value="partes", command=lambda: self.define_funcao(r.get()))
        self.botao_pasta = Button(self.frame, text="Escolha uma pasta", command=self.escolhe_pasta)
        self.botao_arquivo = Button(self.frame, text="Escolha um arquivo", command=self.escolhe_arquivo)
        self.entrada_input = Entry(self.frame)
        self.entrada_texto = Label(self.frame, text="Tamanho máximo (MB)")
        self.botao_dividir = Button(self.frame, text="Dividir", command=self.divide_pdf)
        self.status = Label(self.frame, text="Escolha um arquivo ou pasta.", bd=1, relief=SUNKEN)
        self.botao_info = Button(self.frame, text="Informações", command=self.info_popup)

        self.radio_tam.select()

        self.radio_tam.grid(row=0, column=0, pady=10)
        self.radio_partes.grid(row=0, column=1, pady=10)
        self.botao_pasta.grid(row=1, column=0, pady=10)
        self.botao_arquivo.grid(row=1, column=1, pady=10)
        self.entrada_input.grid(row=2, column=0, pady=10)
        self.entrada_texto.grid(row=2, column=1, pady=10)
        self.botao_dividir.grid(row=3, column=0, columnspan=2, pady=10)
        self.status.grid(row=4, column=0, columnspan=2, pady=10, sticky=W+E)
        self.botao_info.grid(row=5, column=0, columnspan=2, pady=10)


    def divide_pdf(self):
        try:
            tam = self.define_tamanho_maximo()
        except ValueError:
            self.popup("Erro", "Por favor insira um número inteiro maior que zero.")
            return

        self.set_status("Carregando...")
        try:
            control(tam, self.caminho, self.funcao_divisao)
        except AttributeError:
            self.popup("Erro", "Por favor escolha um arquivo ou pasta.")
            self.set_status("Escolha um arquivo ou pasta.")
            return
        except EmptyFileError:
            self.popup("Erro", EMPTY_FILE)
            self.set_status("Escolha um arquivo ou pasta.")
            return
        except FileExistsError:
            self.popup("Erro", PASTA_JA_EXISTE)
            self.set_status("Escolha um arquivo ou pasta.")
            return
        except TooFewPagesError:
            self.popup("Erro", TOO_FEW_PAGES)
            self.set_status("Escolha um arquivo ou pasta.")
            return
        else:
            self.set_status("Sucesso")


    def define_funcao(self, funcao):
        self.entrada_texto.destroy()
        if funcao == "tamanho":
            self.funcao_divisao = 'tamanho'
            self.entrada_texto = Label(self.frame, text="Tamanho máximo (MB)")
        elif funcao == "partes":
            self.funcao_divisao = 'partes'
            self.entrada_texto = Label(self.frame, text="Número de partes")
        self.entrada_texto.grid(row=2, column=1, pady=10)


    def escolhe_pasta(self):
        self.caminho = filedialog.askdirectory(initialdir="./", title="Escolha uma pasta")
        self.set_status(self.caminho)


    def escolhe_arquivo(self):
        self.caminho = filedialog.askopenfilename(initialdir="./", title="Escolha um arquivo", filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
        self.set_status(self.caminho)


    def define_tamanho_maximo(self):
        tam = int(self.entrada_input.get())
        if tam <= 0:
            raise ValueError
        return tam


    def set_status(self, texto):
        self.status.destroy()
        self.status = Label(self.frame, text=texto, bd=1, relief=SUNKEN)
        self.status.grid(row=4, column=0, columnspan=2, pady=10, sticky=W+E)


    def popup(self, title, texto):
        messagebox.showerror(title, texto)


    def info_popup(self):
        top = Toplevel()
        top.title("Informações splitPDF")
        top_label = Label(top, text=TEXTO_INFO).pack()
        botao_fechar = Button(top, text="Fechar", command=top.destroy).pack()


def main():
    root = Tk()
    root.title("splitPDF")
    Pdf(root)
    root.mainloop()


if __name__ == "__main__":
    main()
