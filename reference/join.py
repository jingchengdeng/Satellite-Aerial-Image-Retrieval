#!/usr/bin/python

import tool, sys, io, time, logging
from PIL import Image

class Joining():
    
    tileWidth = 256
    tileHeight = 256
    maxTileNumber = 200
    numSubdomains = 0

    #map tile system
    def joining(self, boundBox):
        zoom = self.getMaxZoom(boundBox)
        #convert latitude and longitude to tile coordinates
        (bottom, left) = tool.toTileCoords(boundBox[1], boundBox[0], zoom)
        (top, right) = tool.toTileCoords(boundBox[3], boundBox[2], zoom)

        #calculate the total number of tiles    
        numXTiles = right-left + 1
        numYTiles = bottom-top + 1
        numTiles = numXTiles * numYTiles
        if (numTiles > self.maxTileNumber):
            logging.error("Maximum number of tiles (%s) is exceeded" %self.maxTileNumber)
            sys.exit(-1)

        #create and download image    
        resultImage = Image.new("RGB", (numXTiles*self.tileWidth, numYTiles*self.tileHeight),(0,0,0,0))
        self.doJoining(left, bottom, right, top, zoom, resultImage, numTiles)
        outputFileName = time.strftime('%m%d%Y-%H%M%S')+ '.png'
        resultImage.save(outputFileName)

    #joining all tile images together
    def doJoining(self, left, bottom, right, top, zoom, resultImage, numTiles):
        counter = 0
        for x in range(left, right+1):
            for y in range(top, bottom+1):
                print('Proccing image %s out of %s' % (counter + 1, numTiles))
                tile = self.getTileImage(zoom, x, y, counter)
                image = Image.open(io.BytesIO(tile))
                resultImage.paste(image, ((x-left)*self.tileWidth, (y-top)*self.tileHeight))
                counter +=1
