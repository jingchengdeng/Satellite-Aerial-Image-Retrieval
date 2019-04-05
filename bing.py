import sys, math, logging, json, mpmath, io
from urllib import request, error
from PIL import Image

class Bing():
    def __init__(self):
        self.dataPath = "http://dev.virtualearth.net/REST/v1/Imagery/Metadata/Aerial"
        self.myKey = "AvHyA8kJY_qxax2ciNHnW61HCz6GxqM6wZr2sLIMYCpsVYSb8BVmJCauCSKLS_5p"
        self.imageUrl = None
        self.imageUrlSubdomains = None
        self.imageWidth = None
        self.imageHeight = None
        self.zoomMax = None
        self.numSubdomains = None
        self.radius = 6378137
        self.blockWidth = 256
        self.blockHeight = 256
        self.maxBlocksAllowed = 256
        self.getData()
    
    def getJson(self, url):
        try:
            return json.loads(request.urlopen(url).read())
        except error.URLError as e:
            if hasattr(e, "reason"):
                logging.error("Faild in getting data: " + e.reason)
            elif hasattr(e, "code"):
                logging.error("Error code: " + e.code)
            sys.exit()
        except:
            logging.error("Wrong request.")
        return
    
    def getData(self):
        res = self.getJson("%s?key=%s" % (self.dataPath, self.myKey))
        if "errorDetails" not in res:
            data = res["resourceSets"][0]["resources"][0]
            self.imageWidth = data["imageWidth"]
            self.imageHeight = data["imageHeight"]
            self.imageUrl = data["imageUrl"]
            self.imageUrlSubdomains = data["imageUrlSubdomains"]
            self.zoomMax = data["zoomMax"]
            self.numSubdomains = len(self.imageUrlSubdomains)
        else:
            logging.error("Unknown response")
            sys.exit()
        # print("data get")
        return
    
    def latLonToXY(self, lat, lon):
        x = math.radians(lon) * self.radius
        y = math.log(math.tan(math.radians(lat)) + mpmath.sec(math.radians(lat))) * self.radius
        # print("calculate from lat lon to x y.")
        return y, x
    
    def xYtoLatLon(self, y, x):
        lat = math.degrees(math.atan(math.sinh(y / self.radius)))
        lon = math.degrees(x / self.radius)
        # print("calculate from x y to lat lon")
        return lat, lon
        
    def quadKey(self, x, y, zoom):
        res = ""
        for i in range(zoom, 0, -1):
            digit = 0
            mask = 1 << (i - 1)
            if x & mask:
                digit += 1
            if y & mask:
                digit += 2
            res += str(digit)
        # print("get quadKey = %s" % res)
        return res
        
    def getMaxZoom(self, coord):
        y_1, x_1 = self.latLonToXY(coord[1], coord[0])
        y_2, x_2 = self.latLonToXY(coord[3], coord[2])
        center_lat, center_lon = self.xYtoLatLon((y_1 + y_2)/ 2, (x_1 + x_2)/ 2)
        zoom = self.zoomMax
        while True:
            res = self.getJson(self.dataPath + '/' + str(center_lat) + ',' + str(center_lon) + "?zl=" + str(zoom) + '&key=' + self.myKey)
            if 'errorDetails' not in res:
                data = res["resourceSets"][0]["resources"][0]
                if data["vintageEnd"]: break
            else:
                logging.error("Unknown response")
                sys.exit()
            zoom -= 1
        # print("get max zoom as %s" % zoom)
        return zoom
        
    def toBlockCoords(self, lat, lon, zoom):
        perimeter = math.pi * self.radius * 2
        blockPerAxis = 2 ** zoom
        y, x = self.latLonToXY(lat, lon)
        norm_lat = perimeter/2 - y
        norm_lon = perimeter/2 + x
        y = norm_lat * blockPerAxis / perimeter
        x = norm_lon * blockPerAxis / perimeter
        # print("get block coords %s, %s" % (x, y))
        return math.floor(y), math.floor(x)
    
    def getBlockUrl(self, zoom, x, y, counter):
        quadkey = self.quadKey(x, y, zoom)
        url = self.imageUrl.replace("{subdomain}", self.imageUrlSubdomains[counter % self.numSubdomains])
        url = url.replace("{quadkey}", quadkey)
        # print("get url at %s" % url)
        return url
        
    def getBlockImage(self, zoom, x, y, counter):
        url = self.getBlockUrl(zoom, x, y, counter)
        try:
            image = request.urlopen(url).read()
        except Exception as e:
            logging.error(e)
            logging.error("Unable to download image with url:" + url)
            sys.exit()
        # print("block image get")
        return image
    
    def merge(self, left, right, top, bottom, zoom, result, numBlocks):
        counter = 0
        for x in range(left, right + 1):
            for y in range(top, bottom + 1):
                print("Image " + str(counter+1) + " in processing, " + str(numBlocks) + " in total.")
                block = self.getBlockImage(zoom, x, y, counter)
                image = Image.open(io.BytesIO(block))
                result.paste(image, ((x - left) * self.blockWidth, (y - top) * self.blockHeight))
                counter += 1
        return
    
    def run(self, input):
        zoom = self.getMaxZoom(input)
        low_lat, high_lat = (input[1], input[3]) if input[1] < input[3] else (input[3], input[1])
        low_lon, high_lon = (input[0], input[2]) if input[0] < input[2] else (input[2], input[0])
        bottom, left = self.toBlockCoords(low_lat, low_lon, zoom)
        top, right = self.toBlockCoords(high_lat, high_lon, zoom)
        # print(bottom, top, left, right)
        numBlocksOnX = right - left + 1
        numBlocksOnY = bottom - top + 1
        numBlocks = numBlocksOnX * numBlocksOnY
        if numBlocks > self.maxBlocksAllowed:
            logging.error("Block number limit exceed by " + numBlocks + ".")
            sys.exit()
        result = Image.new("RGB", (numBlocksOnX * self.blockWidth, numBlocksOnY * self.blockHeight), (0, 0, 0, 0))
        self.merge(left, right, top, bottom, zoom, result, numBlocks)
        fileName = input[4]
        result.save(fileName)
        print("Completed.")
        return