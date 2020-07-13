# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 13:59:52 2020

@author: Sourav
"""


import face_recognition
import cv2
import numpy as np
from gtts import *
import os
import time

def mssg():
    import smtplib 
    from email.mime.multipart import MIMEMultipart 
    from email.mime.text import MIMEText 
    from email.mime.base import MIMEBase 
    from email import encoders
    
    fromaddr = "raspberryp087@gmail.com"     #https://www.google.com/settings/security/lesssecureapps
    toaddr = "shashankshane.demo@gmail.com"
           
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    # storing the senders email address   
    msg['From'] = fromaddr 
      
    # storing the receivers email address  
    msg['To'] = toaddr 
      
    # storing the subject  
    msg['Subject'] = "Subject of the Mail"
    latitude=""
    longitude=""
    # string to store the body of the mail 
    body = "http://www.google.com/maps/place/"+latitude+","+longitude
      
    # attach the body with the msg instance 
    #msg.attach(MIMEText(body, 'plain')) 
      
    # open the file to be sent  
    filename = 'buffer.jpg'
    #attachment = open(filename, "rb") 
      
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 
      
    # To change the payload into encoded form 
    #p.set_payload((attachment).read()) 
      
    # encode into base64 
    #encoders.encode_base64(p) 
         
    # attach the instance 'p' to instance 'msg'
    
    #p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    #msg.attach(p) 
      
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login(fromaddr,"Raspberry@123") 
      
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
      
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    print("mail has been sent")
    # terminating the session 
    s.quit()




one_auth=False
two_auth=False
usernames=['sourav','karthik']
passwords=['pass1','pass2']

username=input("enter the username")

if(username in usernames):
    i=usernames.index(username)
    password=input("enter the password")
    print(password)
    if(password==passwords[i]):
        print("login successful")
        one_auth=True
        video_capture = cv2.VideoCapture(0)
    else:
        print("Incorrect Password")


    p1_image = face_recognition.load_image_file("monu.jpg")
    p1_face_encoding = face_recognition.face_encodings(p1_image)[0]
    
    p2_image = face_recognition.load_image_file("karthik.jpg")
    p2_face_encoding = face_recognition.face_encodings(p2_image)[0]
    
    
    
    
    
    
    known_face_encodings = [
        p1_face_encoding,
        p2_face_encoding
    ]
    known_face_names = [
        "monu",
        "karthik",
    ]
        
                       
 



while(one_auth):

    ret, frame = video_capture.read()

    
    rgb_frame = frame[:, :, ::-1]


    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        print("login successful")
        mytext = 'authorisation successful'
        language='en'
        myobj=gTTS(text=mytext,lang=language,slow=False)
        myobj.save("sample_audio.mp3")
        os.system('start sample_audio.mp3')
        name = "Unknown"                
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            two_auth=True
            

        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

    cv2.imwrite('buffer.jpg',frame)
    cv2.imshow('Video', frame)
    time.sleep(5)
    break


    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_capture.release()
        cv2.destroyAllWindows()
        break

if(one_auth==True and two_auth==True):
    mytext = 'authorisation successful'
    language='en'
    myobj=gTTS(text=mytext,lang=language,slow=False)
    myobj.save("sample_audio.mp3")
    os.system('start sample_audio.mp3')
else:
      mssg()
      mytext = 'authorisation failed'
      language='en'
      myobj=gTTS(text=mytext,lang=language,slow=False)
      myobj.save("sample_audio.mp3")
      os.system('start sample_audio.mp3')
