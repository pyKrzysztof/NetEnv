import json

class Automation:

    def __init__(self):
        pass

    def set_file(self, filepath):
        self.path_to_file = filepath
        self.dictionary = self.load_file()

    def load_file(self):
        with open(self.path_to_file, 'r') as f:
            return json.load(f)

    def get_script_info(self, name):
        if name in self.dictionary:
            return self.dictionary[name]
        return 0

    def get_script(self, name):
        data = self.get_script_info(name)
        print(data)

    def check_if_script(self, name):
        if not self.get_script_data(name):
            return False
        return True