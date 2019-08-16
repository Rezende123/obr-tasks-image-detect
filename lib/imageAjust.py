import cv2

def prepare(image):
    resized = imageResize(image)
    spined = imageSpin(resized)

    return spined

def imageResize(image):
    r = 800.0 / image.shape[1]
    dim = (800, int(image.shape[0] * r))
    
    # perform the actual resizing of the image and show it
    return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def imageSpin(image):    
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    
    # rotate the image by 180 degrees
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    return cv2.warpAffine(image, M, (w, h))
