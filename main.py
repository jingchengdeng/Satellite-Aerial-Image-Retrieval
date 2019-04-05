import sys, os, argparse, logging
from bing import Bing
'''
parser = argparse.ArgumentParser()
parser.add_argument("input", help = "Required inputs with first four input lat, lon, lat, lon and fifth input image's file name to be saved; example:32.7058,64.2663,32.7103,64.2668,123.png")
args = parser.parse_args()

input = [i for i in args.input.split(",")]
for i in range(4):
    input[i] = float(input[i])
'''
input = [-87.635657,41.831554,-87.631949,41.828515,'1.png']
Bing().run(input)