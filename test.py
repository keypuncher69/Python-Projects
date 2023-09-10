import cv2

face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")

img=cv2.imread("95518580-friends-chilling-outside-taking-group-selfie-and-smiling-laughing-young-people-standing-together-out.jpg")

gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces=face_cascade.detectMultiScale(gray_img, scaleFactor=1.04, minNeighbors=5)

for x, y, w, h in faces:
    img=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

resized=cv2.resize(img,(int(img.shape[1]/3),int(img.shape[0]/3)))

print(faces)




cv2.imshow("Gray",resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
