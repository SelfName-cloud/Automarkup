import zipfile


class Unzipper:
    def __init__(self, path_file_zip, path_save_unzip_file):
        self.path_file_zip = path_file_zip
        self.path_save_unzip_file = path_save_unzip_file

        with zipfile.ZipFile(self.path_file_zip, 'r') as f:
            f.extractall(self.path_save_unzip_file)

