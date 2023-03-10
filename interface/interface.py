import tkinter as tk
import tkinter.filedialog as fd
from module_division.division import DivisionDirs


class App(tk.Tk):

    def __init__(self):

        super().__init__()

        btn_dir_input = tk.Button(self, text="Выбрать папку с изображениями",
                                      command=self.choose_directory_input)

        btn_dir_output = tk.Button(self, text="Выбрать папку для размещения",
                                   command=self.choose_directory_output)

        btn_run_program = tk.Button(self, text='Начать',
                                    command=self.run_program)

        btn_dir_input.pack(padx=60, pady=10)
        btn_dir_output.pack(padx=60, pady=10)
        btn_run_program.pack(padx=60, pady=10)

        self.directory_input = ''
        self.directory_output = ''

    def choose_directory_input(self):

        directory = fd.askdirectory(title="Открыть папку", initialdir="/")

        if directory:
            self.directory_input = directory

    def choose_directory_output(self):
        directory = fd.askdirectory(title="Открыть папку", initialdir="/")

        if directory:
            self.directory_output = directory

    def run_program(self):

        print(self.directory_output)
        print(self.directory_input)

        if self.directory_input and self.directory_output:
            division_dirs = DivisionDirs(path_dir_input=self.directory_input, path_dir_output=self.directory_output)
            division_dirs.make_new_dir()
            tk.messagebox.showinfo(title='Ready', message='Markup dataset is ready')
        else:
            # Предупреждение
            tk.messagebox.showwarning(title='Error', message='Select dir with image, please')


if __name__ == "__main__":
    app = App()
    app.mainloop()
