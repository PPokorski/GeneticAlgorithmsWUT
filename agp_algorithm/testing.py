# ! /usr/bin/env python
# coding: utf-8

from PIL import Image
image = Image.open('C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/pictures/mapa.png')
mask = image.convert("L")
th = 150 # the value has to be adjusted for an image of interest
mask = mask.point(lambda i: i < th and 255)

mask.show()

