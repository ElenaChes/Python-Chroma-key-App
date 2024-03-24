#============================IMPORTS================================
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
folder_path = os.getcwd()

#============================FUNCTIONS==============================
# Read input
def getFilenames():
  if len(sys.argv) < 3:
    print("Missing arguments, run this program using the following syntax:\n"+
          "\"python app.py img_filename bk_filename ofilename\"\n"+
          "- img_filename - path to an image with a 'green screen'.\n"+
          "- bk_filename - path to the background.\n"+
          "- ofilename - path to save the edited image, if none is provided it'll be displayed instead.")
    exit() 
  img_filename = sys.argv[1].replace("/", "\\")
  bk_filename = sys.argv[2].replace("/", "\\")
  ofilename = sys.argv[3].replace("/", "\\") if (len(sys.argv) >= 4) else None
  return (img_filename,bk_filename,ofilename)  

#===================================================================
# Read images and check valid paths
def getImgs(img_filename,bk_filename):
  # using "if" instead or "try-except" because cv2.imread doesn't throw exception
  img = cv2.imread(img_filename, cv2.IMREAD_COLOR)
  if img is None:
    print("Couldn't find an image in path: "+folder_path+"\\"+img_filename+".")
    exit() 
  img_bg = cv2.imread(bk_filename, cv2.IMREAD_COLOR)
  if img_bg is None:
    print("Couldn't find an image in path: "+folder_path+"\\"+bk_filename+".")
    exit()
  return (img,img_bg)  

#===================================================================
# Replace green screen       
def processImgs(img,img_bg):
  # Detect the green screen
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  green = np.uint8([[[0, 255, 0]]])
  hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
  h = hsv_green[0][0][0]

  # Create a mask without the green screen
  # (35,50,50) ~ (85,255,255)
  lowerb = np.array([h-25, 50, 50], dtype = "uint8")
  upperb = np.array([h+25, 255, 255], dtype = "uint8")
  img_mask = cv2.inRange(hsv, lowerb, upperb)

  # Smooth mask edges
  img_mask = cv2.medianBlur(img_mask,7)

  # Creating the background image
  img_bgMasked = cv2.bitwise_and(img_bg, img_bg, mask = img_mask) 

  # Removing the green from the original image
  img_invMask = cv2.bitwise_not(img_mask)
  img_masked = cv2.bitwise_and(img, img, mask = img_invMask) 

  # Combining the images
  img_output = cv2.bitwise_or(img_bgMasked, img_masked) 
  return img_output

#===================================================================
# Try to save or display
def saveImg(ofilename,img_output):
  # if ofilename exists, tries to save
  # if ofilename wasn't given or save failed -> imshow()
  if ofilename is not None:
    try:
      saved = cv2.imwrite(ofilename, img_output)
      if saved:
        print("Created "+folder_path+"\\"+ofilename+".")
        return
      print("Couldn't save the image in path: "+folder_path+"\\"+ofilename+", displaying instead.")
    except Exception as error:
      #print (error)
      print("Couldn't save the image in path: "+folder_path+"\\"+ofilename+", displaying instead.")
  else:
    print("Wasn't given a path for the output image, displaying instead.")
    
  # Didn't save, display image 
  plt.subplots(1,1, num="Output Image", constrained_layout=True)
  b,g,r=cv2.split(img_output)
  img = cv2.merge((r, g, b))
  plt.imshow(img) ;plt.subplot(111); plt.axis("off")
  plt.show()

#==============================MAIN=================================
def main():
  # Read input
  img_filename,bk_filename,ofilename = getFilenames()

  # Read images
  img,img_bg = getImgs(img_filename,bk_filename)

  # Make sure images are the same size  
  img_bg = cv2.resize(img_bg, (img.shape[1], img.shape[0]))

  # Replace green screen
  img_output = processImgs(img,img_bg)

  # Try to save or display
  saveImg(ofilename,img_output)
  plt.show()

#===================================================================  
if __name__ == "__main__":
  main()