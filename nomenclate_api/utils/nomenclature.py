import operator
from nomenclate import Nom


class Nomenclate:
    def __init__(self):
        self.instance = Nom()

    def overwite_config(self, config: dict):
        self.instance.config_file_contents = sorted(d.items(), key=operator.itemgetter(1))

    def __str__(self):
        return str(self.instance)

    @getattr
    def data(self):
        return self.instance


instance = Nom()
