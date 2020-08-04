import cv2
import numpy as np
from scipy.ndimage import interpolation as inter
from scipy.spatial import distance as dist
from PIL import Image
# import pytesseract
import copy
class SkewCorrection_and_Warp:
    def __init__(self):
        self.plate=None
        self.contours=None
        self.imgRS=None
        self.imgRT=None
        self.pts=[]
        self.count=0
        self.resize=None
        self.ResArr=[]
        self.origRT=None

    def StartProcess(self, Plate):
        print("1")
        # pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        self.plate=Plate
        # self.count=count
        self.imgRS = cv2.resize(Plate, (400, 150), fx = 1.87, fy = 1.97,interpolation=cv2.INTER_LINEAR)
        angle, rotated = self.Rotate()
        print("angle:",angle)
        self.imgRT = cv2.resize(rotated, (400, 150), fx = 1.87, fy = 1.97,interpolation=cv2.INTER_LINEAR)
        self.origRT=self.imgRT
        self.get_bounding_box()
        def getArea(x):
            h, w, _ = x.shape
            return h*w
        newRes=[]
        print("2")
        iterArr=copy.deepcopy(self.ResArr)
        print("3")
        self.maxCnts=[]
        i=0
        for x in iterArr:
            if(self.hasRT(x)):
                # self.resArr=[]
                # self.max=[]
                # self.imgRS=x
                # anglex, self.imgRT = self.Rotate()
                # self.get_bounding_box()
                # for y in self.ResArr:
                #     if(self.hasRT(y)):
                anglex, self.imgRT = self.Rotate()
                newRes.append(self.imgRT)
                i+=1
            if(i==3):
                break
        print("4")
        finalResArr=[]
        op=[]
        print(len(newRes))
        for x in newRes:
            h, w, _ = x.shape

            # h = x.size().height
            if(w*h < 50000 and w*h>7000):
                finalResArr.append(x)
            elif(w*h>7000):
                op.append(x)
        sorted(op,key=getArea,reverse=True)
        print("5")
        if(len(finalResArr)<1 and len(op)>0):
            finalResArr.append(op[0])
        elif(len(op)==0):
            finalResArr.append(self.origRT)
            # newRes2=[]
            # iterArr2=copy.deepcopy(newRes)
            # self.maxCnts=[]
            # for x in iterArr2:
            #     self.resArr=[]
            #     self.imgRS=x
            #     anglex, self.imgRT = self.Rotate()
            #     self.get_bounding_box()
            #     for y in self.ResArr:
            #         if(self.hasRT(y)):
            #             newRes2.append(y)
            
            # finalResArr=[]
            # op=[]
            # for x in newRes2:
            #     h, w, _ = x.shape
    
            #     # h = x.size().height
            #     if(w*h < 35000 and w*h>8000):
            #         finalResArr.append(x)
            #     elif(w*h>8000):
            #         op.append(x)
        sorted(finalResArr, key=getArea, reverse=True)
        return finalResArr[0]
        # if(self.maxCnts):
        #     cnts = sorted(self.maxCnts, key=cv2.contourArea, reverse=True)
        #     if(len(cnts)>1):
        #         c=cnts[1]
        #     else:
        #         c=cnts[0]
        #     self.origMax.append(c)
        
        #####################################################################
        
        # newRes2=[]
        # iterArr2=copy.deepcopy(newRes)
        # self.maxCnts=[]
        # for x in iterArr2:
        #     self.max=[]
        #     self.imgRS=x
        #     anglex, self.imgRT = self.Rotate()
        #     #self.imgRT = cv2.resize(r, (400, 150), fx = 1.87, fy = 1.97,interpolation=cv2.INTER_LINEAR)
        #     if(sel)
        #     self.get_bounding_box()
        # #c = min(self.maxCnts, key = cv2.contourArea)
        # cnts = sorted(self.maxCnts, key=cv2.contourArea, reverse=True)
        # if(self.maxCnts):
        #     cnts = sorted(self.maxCnts, key=cv2.contourArea, reverse=True)
        #     if(len(cnts)>1):
        #         c=cnts[1]
        #     else:
        #         c=cnts[0]
        #     self.origMax.append(c)   
        # finalRes=[]
        # b,area=self.find_c(2)
        # if(area):
        #     maxa=max(area)
        #     print(maxa)
        #     q=0
        #     indxArea=area.index(maxa)
        #     for i in b:
        #         if(q==indxArea):
        #             self.rect=cv2.minAreaRect(self.maxCnts[i])
        #             imgC = self.crop_and_warp()
        #             text = pytesseract.image_to_string(imgC)
        #             #cv2.imshow("text",imgC)
        #             cv2.waitKey(0)
        #             if(len(text)>0):
        #                 finalRes.append(imgC)
        #             else:
        #                 if(self.origMax):
        #                     c = max(self.origMax, key = cv2.contourArea)
        #                     self.rect=cv2.minAreaRect(c)
        #                     imgC = self.crop_and_warp()
        #                     #cv2.imshow("atp",imgC)
        #                     cv2.waitKey(0)
        #                     finalRes.append(imgC)
        #                 else:
        #                     finalRes.append(self.origRT)
        #         q+=1
        # else:
        #     finalRes.append(self.origRT)
        # if(len(iterArr)>1):
        #     pass
        #         # img1 = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
        #         # img = Image.fromarray(img1)
        #         # im= img.filter(ImageFilter.MedianFilter())
        #         # enhancer = ImageEnhance.Contrast(im)
        #         # im = enhancer.enhance(2)
        #         # text = pytesseract.image_to_string(im)
                
        #         # if(len(text)>0):
        #         #     newRes.append(x)
        # else:
        #     newRes=iterArr
        # if(len(newRes)==0):
        #     print("YES")
        #     newRes=self.max_c
        # if(len(newRes)>1):
        #     print("1")
            
    
    def hasRT(self,x):
        gray = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        
        ctrs, hier = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        count=0
        for i, ctr in enumerate(sorted_ctrs):
            x, y, w, h = cv2.boundingRect(ctr)
        
            #roi = x[y:y + h, x:x + w]
        
            area = w*h
        
            if 800 < area < 6700:
                count+=1

        if(count>=5):
            return True
        else:
            return False
    def Rotate(self, delta=1, limit=50):
        def determine_score(arr, angle):
            data = inter.rotate(arr, angle, reshape=True, order=3)
            histogram = np.sum(data, axis=1)
            score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
            return histogram, score

        gray = cv2.cvtColor(self.imgRS, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 
    
        scores = []
        angles = np.arange(-limit, limit + delta, delta)
        for angle in angles:
            histogram, score = determine_score(thresh, angle)
            scores.append(score)
    
        best_angle = angles[scores.index(max(scores))]
    
        (h, w) = self.imgRS.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        rotated = cv2.warpAffine(self.imgRS, M, (w, h), flags=cv2.INTER_CUBIC, \
                  borderMode=cv2.BORDER_REPLICATE)

        return best_angle, rotated
    
    def get_bounding_box(self):
        imgray = cv2.cvtColor(self.imgRT, cv2.COLOR_BGR2GRAY)
        image_blurred = cv2.GaussianBlur(imgray,(5,5),0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        close = cv2.morphologyEx(image_blurred, cv2.MORPH_CLOSE, kernel, iterations=3)
        thresh = cv2.adaptiveThreshold(close, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 2)
        self.contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        bestCs,areas=self.find_c()
        # if(len(areas)<=1):
        #     self.contours=self.doover()
        #     best2,area2=self.find_c()
            
        #     if(len(area2)==0):
        #         print("fail")
        #         self.ResArr.append(self.imgRT)
        #         # self.max_c.append(self.imgRT)
        #     else:
        #         # sort2=area2
        #         # sort2.sort()
        #         # maxarea=sort2[0]
        #         # opposs=False
        #         # if(len(sort2)>1):
        #         #     opposs=True
        #         #     maxarea2=sort2[1]
        #         #     indexArea2=area2.index(maxarea2)
        #         # a=0
        #         # indxArea1=area2.index(maxarea)
                
        #         # x=0
        #         for i in best2:
        #             self.rect=cv2.minAreaRect(self.contours[i])
        #             imgC = self.crop_and_warp()
        #             # if(a==indxArea1):
        #             #     print("YES")
        #             #     if(self.hasRT(imgC)):
        #             #         self.max_c.append(imgC)
        #             #         self.maxCnts.append(self.contours[i])
        #             #     else:
        #             #         self.max_c.append(self.imgRT)
        #             # if(opposs and a==indexArea2 and self.hasRT(imgC)):
        #             #     self.op.append(imgC)
        #             #     self.maxCnts.append(self.contours[i])
        #             # else:
        #             #         self.max_c.append(self.imgRT)
                    
        #             # cv2.imshow('warp'+str(i),imgC)
        #             # cv2.waitKey(0)
        #             print("corr")
        #             #cv2.imwrite("C:/Users/bhaga/Desktop/SIH/test/warped"+str(self.count)+"_"+str(x)+".jpg",imgC)
        #             self.ResArr.append(imgC)
                    
        # else:
        for i in bestCs:
            self.rect=cv2.minAreaRect(self.contours[i])
            imgC = self.crop_and_warp()
            # if(a==indxArea1):
            #     print("YES")
            #     if(self.hasRT(imgC)):
            #         self.max_c.append(imgC)
            #         self.maxCnts.append(self.contours[i])
            #     else:
            #         self.max_c.append(self.imgRT)
            # if(opposs and a==indxArea1 and self.hasRT(imgC)):
            #     self.op.append(imgC)
            #     self.maxCnts.append(self.contours[i])
            # else:
            #     self.max_c.append(self.imgRT)
            
            #cv2.imwrite("C:/Users/bhaga/Desktop/SIH/test/warped"+str(self.count)+"_"+str(x)+".jpg",imgC)
            self.ResArr.append(imgC)
            
    def find_c(self,round=1):
        bestCs=[]
        areas=[]
        cnt=self.contours
        if(round==2):
            cnt=self.maxCnts
        for i,c in enumerate(cnt):
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            self.pts=box
            rbox = self.order_points()
            w = np.linalg.norm([rbox[0, 0] - rbox[1, 0], rbox[0, 1] - rbox[1, 1]])
            h = np.linalg.norm([rbox[0, 0] - rbox[-1, 0], rbox[0, 1] - rbox[-1, 1]])
            aspect_ratio = float(w)/h
            area=w*h
            if(area>8000 and aspect_ratio>2):
                areas.append(w*h)
                bestCs.append(i)
        return bestCs,areas
    
    def order_points(self):
        xSorted = self.pts[np.argsort(self.pts[:, 0]), :]
        leftMost = xSorted[:2, :]
        rightMost = xSorted[2:, :]
        leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
        (tl, bl) = leftMost
        D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
        (br, tr) = rightMost[np.argsort(D)[::-1], :]
        return np.asarray([tl, tr, br, bl], dtype=self.pts.dtype)

    def doover(self):
        img2=self.make_small()
        imgray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(imgray)
        bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 27, -7)
        horizontal = np.copy(bw)
        vertical = np.copy(bw)
        cols = horizontal.shape[1]
        horizontal_size = cols // 400
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
        horizontal = cv2.erode(horizontal, horizontalStructure)
        horizontal = cv2.dilate(horizontal, horizontalStructure)
        rows = vertical.shape[0]
        verticalsize = rows // 150
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
        vertical = cv2.erode(vertical, verticalStructure)
        vertical = cv2.dilate(vertical, verticalStructure)
        vertical = cv2.bitwise_not(vertical)
        edges = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 33, -3)
        kernel = np.ones((11, 11), np.uint8)
        edges = cv2.dilate(edges, kernel)
        smooth = np.copy(vertical)
        smooth = cv2.blur(smooth, (5, 5))
        (rows, cols) = np.where(edges != 0)
        vertical[rows, cols] = smooth[rows, cols]
        thresh = cv2.adaptiveThreshold(vertical, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, -3)
        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def make_small(self):
        x, y = 403,153
        img1 = cv2.cvtColor(self.imgRT, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img1)
        new = img.resize((x, y), Image.ANTIALIAS)
        new2 = img.resize((x, y), Image.ANTIALIAS)
        new.paste(img, (int((x - 400) / 2), int((y - 150) / 2)))
        result = Image.blend(new, new2, alpha=0.5)
        rgb_im = result.convert('RGB')
        resiz= rgb_im.resize((400, 150), Image.ANTIALIAS)
        i, j = 397,147
        new3 = img.resize((i, j), Image.ANTIALIAS)
        new4 = img.resize((i, j), Image.ANTIALIAS)
        new3.paste(img, (int((400-i) / 2), int((150-j) / 2)))
        result2= Image.blend(new3, new4, alpha=0.5)
        rgb_im2 = result2.convert('RGB')
        resiz2= rgb_im2.resize((400, 150), Image.ANTIALIAS)
        nr= Image.blend(resiz, resiz2, alpha=0.5)
        opencvImage = cv2.cvtColor(np.array(nr), cv2.COLOR_RGB2BGR)
        return opencvImage
    
    def crop_and_warp(self):
        self.pts=cv2.boxPoints(self.rect)
        rbox = self.order_points()
        width = np.linalg.norm([rbox[0, 0] - rbox[1, 0], rbox[0, 1] - rbox[1, 1]])
        height = np.linalg.norm([rbox[0, 0] - rbox[-1, 0], rbox[0, 1] - rbox[-1, 1]])
        src = rbox.astype(np.float32)
        dst = np.array([[0, 0],
                                [width - 1, 0],
                                 [width - 1, height - 1],
                                 [0, height - 1]], dtype="float32")
        m = cv2.getPerspectiveTransform(src, dst)
        return cv2.warpPerspective(self.imgRT, m, (width, height))
    
    # def image_resize(self, desired_size, inter = cv2.INTER_AREA):
    #     print(self.resize)
    #     old_size = self.resize.shape[:2] # old_size is in (height, width) format

    #     ratio = float(desired_size)/max(old_size)
    #     new_size = tuple([int(x*ratio) for x in old_size])
        
    #     # new_size should be in (width, height) format
        
    #     im = cv2.resize(self.resize, (new_size[1], new_size[0]))
        
    #     delta_w = desired_size - new_size[1]
    #     delta_h = desired_size - new_size[0]
    #     top, bottom = delta_h//2, delta_h-(delta_h//2)
    #     left, right = delta_w//2, delta_w-(delta_w//2)
        
    #     color = [0, 0, 0]
    #     new_im = cv2.copyMakeBorder(self.resize, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

    #     return new_im