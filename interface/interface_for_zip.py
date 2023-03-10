import tkinter as tk
import tkinter.filedialog as fd
from module_division.division import DivisionDirs
from unzipper import Unzipper


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        btn_select_file = tk.Button(self, text='Выбрать файл', command=self.choose_file_zip)

        btn_dir_output = tk.Button(self, text="Выбрать папку для размещения",
                                   command=self.choose_directory_output)

        btn_run_program = tk.Button(self, text='Начать', command=self.run_program)

        btn_select_file.pack(padx=60, pady=10)
        btn_dir_output.pack(padx=60, pady=10)
        btn_run_program.pack(padx=60, pady=10)

        self.filename = ''
        self.directory_output = ''

    def choose_file_zip(self):
        file = fd.askopenfilename(initialdir='/', title='Выбрать файл', filetypes=[("Zip files", ".zip"), ("Tar.gz files", "tar.gz"), ('7z files', '.7z')])

        if file:
            print(file)
        self.filename = file

    def choose_directory_output(self):
        directory = fd.askdirectory(title="Открыть папку", initialdir="/")

        if directory:
            self.directory_output = directory

    def run_program(self):
        if self.filename and self.directory_output:
            directory_unzip = '/home/nikita/PycharmProjects/ProjectVKR/saved'
            Unzipper(path_file_zip=self.filename, path_save_unzip_file=directory_unzip)
            division_dirs = DivisionDirs(path_dir_input=directory_unzip + '/dataset', path_dir_output=self.directory_output)
            division_dirs.make_new_dir()
            tk.messagebox.showinfo(title='Ready', message='Markup dataset is ready')
        else:
            print('Что то не так!')
            tk.messagebox.showwarning(title='Error', message='Select .zip /.tar.gz / .7z files, please')


if __name__ == "__main__":
    app = App()
    app.mainloop()