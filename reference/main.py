#!/usr/bin/python

import sys, os, argparse, logging

from bing import Bing

#passing the parameters from the command line to the function
parser = argparse.ArgumentParser()
parser.add_argument("bbox", help="boundbox coordinates in the form left,bottom,right,top; example:16.7058,48.2663,16.71037,48.2668 ")
#parser.add_argument("-z", "--zoom", type=int, help="zoom level")
args = parser.parse_args()

# preparing bbox
bbox = [float(i) for i in args.bbox.split(",")]
Bing().joining(bbox)
