import cv2

def main() :
    imgs = []
    imgs.append(cv2.imread(input("Image1 : ")))
    imgs.append(cv2.imread(input("Image2 : ")))

    hists = []

    for img in imgs:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX) 
        hists.append(hist)

    query = hists[0]
    ret = cv2.compareHist(query, hists[1], cv2.HISTCMP_BHATTACHARYYA)
    print('How Different (0 = Same Image, 1 = Totally Different Image) : ', ret)
        
if __name__ == "__main__" :
    main()
