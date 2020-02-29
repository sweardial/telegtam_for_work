import face_recognition


image = face_recognition.load_image_file('/Users/ross/Desktop/telegtam_for_work/file_7.jpg')
face_location = face_recognition.face_locations(image)
print(face_location)






