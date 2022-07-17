from numpy import imag
from utils import video_image
from utils.video_image import *
from utils.stitching import *
from utils.crop_img import *
import os
import cv2

def n_interpolation(vidpath,outvid):
    fps = video_to_images(vidpath,"./Temp")
    name = vidpath.split('/')[-1][:-4]
    images=[]
    cropped=[]
    img_len= len(os.listdir("./Temp")) 

    for img in range(img_len):
        images.append(f"./Temp/{img}.jpg")

    print(images)
    height, width, _ = cv2.imread(images[0]).shape

    for i in range(len(images)-1):
        stitched = stitch(images[i],images[i+1] )
        cropped.append(crop(stitched,height,width))

    real_img=[cv2.imread(img) for img in images]
    all_img=[]
    count_crop = 0
    count_real = 0
    for i in range(1,len(images)+len(cropped)):
        if i%2==0:
            all_img.append(cropped[count_crop])
            count_crop +=1
        elif i%2!=0:
            all_img.append(real_img[count_real])
            count_real +=1
    images_to_video(all_img,outvid,f"{name}_Ninterpolated.mp4",get_output_fps(fps))
    
    flush_image_folder("./Temp")
if __name__=="__main__":
    n_interpolation("./data/test.mp4", "./ha")


