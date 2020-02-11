from mensagens import *
from splitpdf_l import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class Pdf(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.frame = LabelFrame(text="Divisor de PDFs", padx=50, pady=50)
        self.frame.pack()

        self.botao_pasta = Button(self.frame, text="Escolha uma pasta", command=self.escolhe_pasta)
        self.botao_arquivo = Button(self.frame, text="Escolha um arquivo", command=self.escolhe_arquivo)
        self.tamanho_input = Entry(self.frame)
        self.tamanho_texto = Label(self.frame, text="Tamanho máximo (MB)")
        self.botao_dividir = Button(self.frame, text="Dividir", command=self.divide_pdf)
        self.status = Label(self.frame, text="Escolha um arquivo ou pasta.", bd=1, relief=SUNKEN)
        self.botao_info = Button(self.frame, text="Informações", command=self.info_popup)


        self.botao_pasta.grid(row=0, column=0, pady=10)
        self.botao_arquivo.grid(row=0, column=1, pady=10)
        self.tamanho_input.grid(row=1, column=0, pady=10)
        self.tamanho_texto.grid(row=1, column=1, pady=10)
        self.botao_dividir.grid(row=2, column=0, columnspan=2, pady=10)
        self.status.grid(row=3, column=0, columnspan=2, pady=10, sticky=W+E)
        self.botao_info.grid(row=4, column=0, columnspan=2, pady=10)

    def divide_pdf(self):
        tam = self.define_tamanho_maximo()
        try:
            tam = int(tam)
            if tam == 0:
                self.popup("Erro", "Por favor digite um número maior que 0.")
                return
        except ValueError:
            self.popup("Erro", "Por favor insira um número inteiro.")
            return

        try:
            self.set_status("Carregando...")
            control(tam, self.caminho)
            self.set_status("Sucesso")
        except AttributeError:
            self.popup("Erro", "Por favor escolha um arquivo ou pasta.")
            self.set_status("Escolha um arquivo ou pasta.")
            return
        except FileExistsError:
            self.popup("Erro", "Já existe uma pasta com o nome de um dos arquivos selecionados. Renomeie o arquivo ou a pasta")
            self.set_status("Escolha um arquivo ou pasta.")
            return


    def escolhe_pasta(self):
        self.caminho = filedialog.askdirectory(initialdir="./", title="Escolha uma pasta")
        self.set_status(self.caminho)


    def escolhe_arquivo(self):
        self.caminho = filedialog.askopenfilename(initialdir="./", title="Escolha um arquivo", filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
        self.set_status(self.caminho)


    def define_tamanho_maximo(self):
        return self.tamanho_input.get()


    def set_status(self, texto):
        self.status = Label(self.frame, text=texto, bd=1, relief=SUNKEN)
        self.status.grid(row=3, column=0, columnspan=2, pady=10, sticky=W+E)


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
