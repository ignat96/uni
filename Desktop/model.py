import webview
import os


class MainModel:
    __supported_filetypes: list = [
        '.uni',
    ]
    __folder_list = []
    __opened_file = None

    def __init__(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.drives = ['{0}:\\'.format(d) for d in letters if os.path.exists('{0}:'.format(d))]
        self.current_folder = os.path.expanduser("~")
        self.__scan_folder()

    def open_file(self, file: str = None):
        print('b1')
        w = webview.active_window()
        data = {}
        ext = os.path.splitext(file)[1]
        if ext in self.__supported_filetypes:
            self.opened_file = file
            try:
                with open(file, mode='r', encoding='utf-8') as fp:
                    data = fp.read()
            except IOError:
                w.evaluate_js("app.new_alert(519, 'File structure is corrupted')")

        else:
            w.evaluate_js("app.new_alert(517, 'Unsupported file type')")

        return data

    def save_file(self, data, op=2):
        w = webview.active_window()
        # w.evaluate_js(f"alert('{self.opened_file}')")
        # print(os.path.splitext(os.path.basename(self.opened_file))[0])
        # result = w.create_file_dialog(webview.SAVE_DIALOG, directory=self., save_filename="group_name.uni")
        with open(self.opened_file, mode='w+', encoding='utf-8') as fp:
            fp.write(data)

    def open_folder(self, folder="", op=""):
        w = webview.active_window()
        if op == "back":
            if self.current_folder in self.drives:
                self.__folder_list = [{'name': i, 'path': i, 'type': 'd'} for i in self.drives]
                return self.folder_list
            self.current_folder = os.path.dirname(self.current_folder)

        elif folder != '':
            for f in self.folder_list:
                if f['name'] == folder and not os.path.isfile(f['name']):
                    self.current_folder = f['path']
                    break

        self.__scan_folder()
        return self.__folder_list

    @property
    def supported_filtypes(self):
        return self.__supported_filetypes

    @property
    def folder_list(self):
        return self.__folder_list

    @folder_list.setter
    def folder_list(self, value):
        self.__folder_list = value

    @property
    def opened_file(self):
        return self.__opened_file

    @opened_file.setter
    def opened_file(self, value):
        self.__opened_file = value

    def __scan_folder(self):
        w = webview.active_window()
        try:
            os.scandir(self.current_folder)
        except PermissionError:
            w.evaluate_js("app.new_alert(518, 'Permission denied')")
        else:
            self.__folder_list.clear()
            for i in os.scandir(self.current_folder):
                self.__folder_list.append({
                    'name': i.name,
                    'path': i.path,
                    'type': 'd' if i.is_dir() else 'o'
                })
