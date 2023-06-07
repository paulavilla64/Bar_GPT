import os
from Bar_GPT.Repository.CreateDatabase import *

def main():
    db = CreateDatabase()
    db.create()