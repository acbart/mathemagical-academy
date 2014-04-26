import spyral
from title import Title

from model.model import load_resources

def main():
    load_resources()
    spyral.director.push(Title())