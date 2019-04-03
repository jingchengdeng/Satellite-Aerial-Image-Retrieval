#!/usr/bin/python

import sys, math, logging, urllib
import tool
from join import Joining

#convert tile coordinate to quadkey



class Bing(Joining):
    metadataPath = "http://dev.virtualearth.net/REST/v1/Imagery/Metadata/Aerial"
    bingMapsKey = "ApaoUzCK5_6HzEgOsPL_HFxYj-RVA2FAvcvQHX4XKeR6tjzl9lquWXiZSwBFe8h-"
    imageUrl = ""
    imageUrlSubdomains = None
    zoomMax = 21 # max zoom for the whole world
    
    def __init__(self):
        self.getMetadata()
        
    def quadKey(self, x, y, zoom):
        quadKey = ""
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i-1)
            if (x & mask) != 0:
                    digit += 1
            if (y & mask) != 0:
                    digit += 2
            quadKey += str(digit)
        return quadKey
    
    def getMetadata(self):
        response = tool.fetchJson("%s?key=%s" % (self.metadataPath, self.bingMapsKey))
        if "errorDetails" not in response:
            data = response["resourceSets"][0]["resources"][0]
            self.tileWidth = data["imageWidth"]
            self.tileHeight = data["imageHeight"]
            self.imageUrl = data["imageUrl"]
            self.imageUrlSubdomains = data["imageUrlSubdomains"]
            self.zoomMax = data["zoomMax"]
            self.numSubdomains = len(self.imageUrlSubdomains)
        else:
            logging.error("Unknown response from the server")
            sys.exit(-1)

        #get url of the image
    def getTileUrl(self, zoom, x, y, tileCounter):
        quadkey = self.quadKey(x, y, zoom)
        url = self.imageUrl.replace("{subdomain}", self.imageUrlSubdomains[tileCounter % self.numSubdomains])
        url = url.replace("{quadkey}", quadkey)
        return url

        #get the maximum zoom level	
    def getMaxZoom(self, bbox):
        (bottom, left) = tool.toSphMercator(bbox[1], bbox[0])
        (top, right) = tool.toSphMercator(bbox[3], bbox[2])
        (centerY, centerX) = tool.toLatLon((top+bottom)/2, (left+right)/2)
        zoom = self.zoomMax
        while True:
            response = tool.fetchJson("%s/%s,%s?zl=%s&key=%s" % (self.metadataPath, centerY, centerX, zoom, self.bingMapsKey))
            if "errorDetails" not in response:
                data = response["resourceSets"][0]["resources"][0]
                if data["vintageEnd"]: break
            else:
                logging.error("Unknown response from the server")
                sys.exit(-1)
            zoom = zoom-1
        return zoom

        #get the tile image
    def getTileImage(self, zoom, x, y, counter):
        url = self.getTileUrl(zoom, x, y, counter)
        try:
            tile = urllib.request.urlopen(url).read()
        except Exception as e:
            logging.error(e)
            logging.error("Unable to download image %s" % url)
            sys.exit(-1)
        return tile
