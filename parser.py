import argparse

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("process_name", help="Name of the process")

    def parse(self):
        return self.parser.parse_args()
