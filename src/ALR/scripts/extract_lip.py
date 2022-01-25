import sys
import os
import dlib
import glob
import cv2

predictor_path = "../resources/shape_predictor_68_face_landmarks.dat"
faces_folder_path = "data/AVDigits_imgs/S1_0_01"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
# win = dlib.image_window()
i = 0
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    print("Processing file: {}".format(f))
    img = cv2.imread(f)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

    # Find the bounding boxes of each face using detector

    dets = detector(img)
    # print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        i += 1
        # The next lines of code just get the coordinates for the mouth
        # and crop the mouth from the image.This part can probably be optimised
        # by taking only the outer most points. (48,67)
        xmouthpoints = [shape.part(x).x for x in range(48,67)]
        ymouthpoints = [shape.part(x).y for x in range(48,67)]
        maxx = max(xmouthpoints)
        minx = min(xmouthpoints)
        maxy = max(ymouthpoints)
        miny = min(ymouthpoints) 

        # to show the mouth properly pad both sides
        pad = 20
        # basename gets the name of the file with it's extension
        # splitext splits the extension and the filename
        # This does not consider the condition when there are multiple faces in each image.
        # if there are then it just overwrites each image and show only the last image.
        filename = os.path.splitext(os.path.basename(f))[0]

        crop_image = img[miny-pad:maxy+pad,minx-pad:maxx+pad]
        # cv2.imshow('mouth',crop_image)
        # The mouth images are saved in the format 'mouth1.jpg, mouth2.jpg,..
        # Change the folder if you want to. They are stored in the current directory
        cv2.imwrite(filename+'.jpg',crop_image)
        # cv2.waitKey(0)
        cv2.destroyAllWindows()
    #     win.add_overlay(shape)

    # win.add_overlay(dets)