cropImgHorizontal = (2, 101, 798, 73)
cropImgVertical = (232, 2, 357, 598)

def cropHorizontal(img):
    return img[int(cropImgHorizontal[1]):int(cropImgHorizontal[1]+cropImgHorizontal[3]), 
    int(cropImgHorizontal[0]):int(cropImgHorizontal[0]+cropImgHorizontal[2])]

def cropVertical(img):
    return img[int(cropImgVertical[1]):int(cropImgVertical[1]+cropImgVertical[3]), 
    int(cropImgVertical[0]):int(cropImgVertical[0]+cropImgVertical[2])]
    
