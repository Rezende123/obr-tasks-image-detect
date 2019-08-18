cropImg = (2, 101, 798, 73)

def crop(img):
    return img[int(cropImg[1]):int(cropImg[1]+cropImg[3]), int(cropImg[0]):int(cropImg[0]+cropImg[2])]
    
