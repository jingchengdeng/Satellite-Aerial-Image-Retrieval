import sys, os, argparse, logging
from bing import Bing

res = [0] * 5
res[0] = float(input("Please input first latitude:"))
res[1] = float(input("Please input first longitude:"))
res[2] = float(input("Please input second latitude:"))
res[3] = float(input("Please input second longitude:"))
res[4] = str(input("Please input the image file name to be saved:"))

# input = [-87.635657,41.831554,-87.631949,41.828515,'1.png']
Bing().run(res)