#!/usr/bin/python
import json
from functions import make_collage, get_artwork

def main():
    artworks = get_artwork()
    make_collage(artworks)



main()