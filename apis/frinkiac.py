from compuglobal import CompuGlobalAPI


# Simpsons Meme/GIF generator API
class Frinkiac(CompuGlobalAPI):
    def __init__(self):
        super().__init__('https://frinkiac.com/', 'The Simpsons')
