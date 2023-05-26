import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import pytesseract as ocr
from pdf2image import convert_from_path
from textblob import TextBlob
from urllib.parse import quote


class OCRConverter:
    def __init__(self, master):
        self.master = master
        master.title("OCR Converter")

        # Frame para os widgets
        self.ocr_frame = ttk.Frame(master)
        self.ocr_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Label e button para selecionar o PDF a ser transformador em texto
        self.pdf_label = ttk.Label(self.ocr_frame, text="PDF:")
        self.pdf_label.grid(row=0, column=0, pady=(5, 10))

        self.pdf_button = ttk.Button(
            self.ocr_frame, text="Selecionar arquivo", command=self.select_pdf_file, width=20)
        self.pdf_button.grid(row=0, column=1, pady=(5, 10))

        # Label e button para selecionar diretório de saída do texto convertido
        self.outdir_label = ttk.Label(
            self.ocr_frame, text="Diretório de saída:")
        self.outdir_label.grid(row=1, column=0, pady=10)

        self.outdir_button = ttk.Button(
            self.ocr_frame, text="Selecionar pasta", command=self.select_output_dir, width=20)
        self.outdir_button.grid(row=1, column=1, pady=10)

        # Labels e Entry, para capturar quantos graus deseja rotacionar e quais páginas
        self.rotate_label = ttk.Label(
            self.ocr_frame, text="Quantos graus deseja rotacionar?")
        self.rotate_label.grid(row=2, column=0, pady=10)

        self.rotate_entry = ttk.Entry(self.ocr_frame, width=20)
        self.rotate_entry.grid(row=2, column=1, pady=10)

        self.rotate_label2 = ttk.Label(
            self.ocr_frame, text="Quais páginas deseja rotacionar?\n[Separe por vírgula: 1,2,4,7]\nSe for todas, digite: todas")
        self.rotate_label2.grid(row=3, column=0, pady=10)

        self.rotate_entry2 = ttk.Entry(self.ocr_frame, width=20)
        self.rotate_entry2.grid(row=3, column=1, pady=10)

        # Código que define os radio buttons, sobre sentido do direcionamento da rotação
        self.opt_rotate = tk.StringVar()

        self.rb1 = ttk.Radiobutton(
            self.ocr_frame, variable=self.opt_rotate, text="Sentido Anti-Horário", value=False)
        self.rb1.grid(row=4, column=0, pady=(0, 10))

        self.rb2 = ttk.Radiobutton(
            self.ocr_frame, variable=self.opt_rotate, text="Sentido Horário", value=True)
        self.rb2.grid(row=4, column=1, pady=(0, 10))

        # Código que define a lista de opções de linguagens
        self.languages = ["Português", "Inglês", "Grego"]

        # Label para a lista de opções
        self.list_label = tk.Label(
            self.ocr_frame, text="Selecione as linguagens:")
        self.list_label.grid(row=5, column=0, pady=(10, 0))

        # Listbox para a lista de opções
        self.listbox = tk.Listbox(
            self.ocr_frame, selectmode=tk.MULTIPLE, height=3, width=20)
        self.listbox.grid(row=5, column=1, pady=(10, 0))

        # Adiciona as opções de linguagens ao Listbox
        for language in self.languages:
            self.listbox.insert(tk.END, language)

        # Check se irá querer traduzir o texto ou não.
        self.var_check_traction = tk.BooleanVar()
        self.check_traduction = ttk.Checkbutton(
            self.ocr_frame, text=" Traduzir texto? (Somente do inglês)\n Necessário conexão com a internet", variable=self.var_check_traction)
        self.check_traduction.grid(row=6, column=0, columnspan=2, pady=10)

        # Variável para armazenar as seleções do usuário
        self.selections = []
        self.lang_opt = None

        # Código que define o botão para converter o PDF em texto e fazer demais operações nas funcões convert_pdf_to_text
        self.convert_button = ttk.Button(
            self.ocr_frame, text="Converter PDF para texto", command=self.convert_pdf_to_text)
        self.convert_button.grid(
            row=7, column=0, columnspan=2, pady=10, sticky="s")

        # Variáveis para armazenar o arquivo PDF selecionado e o diretório de saída
        self.pdf_file = None
        self.output_dir = None

        # Pega a origem/caminho do executavel
        executable = os.path.dirname(os.path.abspath(__file__))

        path_new = []
        # Configuração do Tesseract OCR
        if "conversor_ocr" in executable:
            ocr.pytesseract.tesseract_cmd = executable+"\\Tesseract-OCR\\Tesseract-OCR\\tesseract.exe"
            for item in executable:
                if item == "\\":
                    path_new.append("/")
                else:
                    path_new.append(item)
            path_new = "".join(path_new)
            self.custom_config = fr'{path_new}/Tesseract-OCR/Tesseract-OCR/tessdata'
            self.poppler_path = executable+'\\poppler-0.68.0\\poppler-0.68.0\\bin'
        else:
            ocr.pytesseract.tesseract_cmd = executable+"\\Tesseract-OCR\\tesseract.exe"
            for item in executable:
                if item == "\\":
                    path_new.append("/")
                else:
                    path_new.append(item)
            path_new = "".join(path_new)
            self.custom_config = fr'{path_new}/Tesseract-OCR/tessdata'
            self.poppler_path = executable+'\\poppler-0.68.0\\bin'

    def select_pdf_file(self):
        self.pdf_file = filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=[
                ("PDF Files", "*.pdf")
                ]
            )
        if self.pdf_file:
            self.pdf_button.config(text=self.pdf_file)

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(
            title="Selecione um diretório de saída")
        if self.output_dir:
            self.outdir_button.config(text=self.output_dir)

    def convert_pdf_to_text(self):
        try:
            if not self.pdf_file:
                raise Exception(
                    "Nenhum arquivo PDF selecionado! Por favor selecione um PDF.")

            if not self.output_dir:
                raise Exception(
                    "Nenhum diretório de saída selecionado! Por favor selecione um local.")

            self.validate_selections_lang()

            pages = convert_from_path(
                pdf_path=self.pdf_file,
                dpi=300,
                poppler_path=self.poppler_path
                )

            for i, page in enumerate(pages):
                result_validate_rotate = self.validate_rotate()
                if result_validate_rotate:
                    if self.rotate_entry2.get().lower() == "todas":
                        if self.opt_rotate.get() == "0":
                            page = page.rotate(int(self.rotate_entry.get()))
                        elif self.opt_rotate.get() == "1":
                            page = page.rotate(-int(self.rotate_entry.get()))
                        else:
                            raise Exception(
                                "Você precisa selecionar um sentido da rotação")
                    else:
                        for item in self.rotate_entry2.get():
                            if item.isnumeric():
                                if int(item) == i+1:
                                    if self.opt_rotate.get() == "0":
                                        page = page.rotate(
                                            int(self.rotate_entry.get()))
                                    elif self.opt_rotate.get() == "1":
                                        page = page.rotate(
                                            -int(self.rotate_entry.get()))
                                    else:
                                        raise Exception(
                                            "Você precisa selecionar um sentido da rotação")
                            elif item != ",":
                                raise Exception(
                                    "Você só pode digitar números separados por vírgula (,)")
                image_filename = os.path.join(
                    self.output_dir, f"page_{i+1}.jpg")
                page.save(image_filename, "JPEG")
                text = ocr.image_to_string(
                    image=Image.open(image_filename),
                    lang=self.lang_opt,
                    config="--tessdata-dir "+self.custom_config
                    )
                text = text.replace('-\n', '')
                text = text.replace("|", "i")
                linhas = text.splitlines()
                text = " ".join(linhas)

                if self.var_check_traction.get():
                    if "eng" in self.lang_opt:
                        tradutor = TextBlob(text)
                        text = str(tradutor.translate(from_lang="en", to="pt"))
                        text = "Saliento que a tradução não é 100%!\n"+text

                text_filename = os.path.join(
                    self.output_dir, f"page_{i+1}.txt")
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                # os.remove(image_filename)
            self.show_message("Conversão concluída com sucesso!")

        except Exception as e:
            self.show_error(f"Erro ao converter PDF para texto: {e}")

    def validate_rotate(self):
        if not self.rotate_entry.get() and not self.rotate_entry2.get():
            return False
        if self.rotate_entry.get():
            if self.rotate_entry2.get():
                pass
            else:
                raise Exception(
                    "Você não colocou nenhuma página para rotacionar!")
        if self.rotate_entry2.get():
            if self.rotate_entry.get():
                if not self.rotate_entry.get().isnumeric():
                    raise Exception(
                        "Você só pode digitar números no grau de rotação.")
                else:
                    pass
            else:
                raise Exception(
                    "Você não colocou nenhum grau para rotação!")
        return True

    def validate_selections_lang(self):
        self.selections = [self.languages[i]
                           for i in self.listbox.curselection()]
        if len(self.selections) == 0:
            raise Exception(
                'Nenhuma linguagem selecionada, por favor selecione uma opção!')
        elif len(self.selections) == 1:
            if 'Português' in self.selections[0]:
                self.lang_opt = 'por'
                return
            elif 'Inglês' in self.selections[0]:
                self.lang_opt = 'eng'
                return
            elif 'Grego' in self.selections[0]:
                self.lang_opt = 'ell'
                return
            else:
                raise Exception(
                    "Erro desconhecido, favor contatar o administrador![2]")
        elif len(self.selections) == 2:
            if 'Português' in self.selections[0]:
                self.lang_opt = 'por'
                if 'Inglês' in self.selections[1]:
                    self.lang_opt = self.lang_opt+'+eng'
                    return
                elif 'Grego' in self.selections[1]:
                    self.lang_opt = self.lang_opt+'+ell'
                    return
                else:
                    raise Exception(
                        "Erro desconhecido, favor contatar o administrador![4]")
            elif 'Inglês' in self.selections[0]:
                self.lang_opt = 'eng'
                if 'Português' in self.selections[1]:
                    self.lang_opt = self.lang_opt+'+por'
                    return
                elif 'Grego' in self.selections[1]:
                    self.lang_opt = self.lang_opt+'+ell'
                    return
                else:
                    raise Exception(
                        "Erro desconhecido, favor contatar o administrador![5]")
            elif 'Grego' in self.selections[0]:
                self.lang_opt = 'ell'
                if 'Português' in self.selections[1]:
                    self.lang_opt = self.lang_opt+'+por'
                    return
                elif 'Inglês' in self.selections[1]:
                    self.lang_opt = self.lang_opt+'+eng'
                    return
                else:
                    raise Exception(
                        "Erro desconhecido, favor contatar o administrador![6]")
            else:
                raise Exception(
                    "Erro desconhecido, favor contatar o administrador![3]")
        elif len(self.selections) == 3:
            self.lang_opt = 'por+eng+ell'
            return
        else:
            raise Exception(
                "Erro desconhecido, favor contatar o administrador![1]")

    def show_error(self, message):
        messagebox.showerror("Erro", message)

    def show_message(self, message):
        messagebox.showinfo("Concluído", message)


root = tk.Tk()
app = OCRConverter(root)
root.mainloop()
