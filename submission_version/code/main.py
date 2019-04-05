import sys, os, argparse, logging
from bing import Bing

res = [0] * 5
res[0] = float(input("Please input first latitude(e.g. -87.624325):"))
res[1] = float(input("Please input first longitude(e.g. 41.884358):"))
res[2] = float(input("Please input second latitude(e.g. -87.620691):"))
res[3] = float(input("Please input second longitude(e.g. 41.880884):"))
res[4] = str(input("Please input the image file name to be saved(e.g. millennium_park.png):"))

# input = [-87.635657,41.831554,-87.631949,41.828515,'1.png']
Bing().run(res)