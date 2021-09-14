from flask import Flask,render_template,Response,request
import cv2
import os
import datetime as datetime,time
from threading import Thread
import jyserver.Flask as jsf
from init import db,app,directory
from models import camera_task, operation

global camera,switch, rec_frame,start_time,end_time,frame
camera = None
switch =0
frame =None

def folder_creat(video_name="output.mp4" ):
    name="video"
    directory=os.path.normpath(os.getcwd() + os.sep + os.pardir)
    os.chdir(directory)
    file_path = os.listdir()
    if name in file_path:
        return os.path.join(directory,name,video_name)
    else:
        os.mkdir(name)
        print(f'Folder "{name}" succesfully created!')
    return os.path.join(directory,name,video_name)


def record(out):
    global rec_frame, frame
    rec_frame =frame
    while True:
        time.sleep(0.05)
        out.write(rec_frame)


def generate_frames():
    global rec_frame, camera,frame
    if camera is None:
        pass
    else:
        while True:
            success,frame=camera.read()
            if not success:
                break
            else:
                rec_frame=frame
                frame=cv2.flip(frame,1)
                ret,buffer=cv2.imencode('.jpg',frame)
                frames=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames + b'\r\n')


@jsf.use(app)
class App:
    def __init__(self):
        
        self.startTime= 0
        self.stopTime =0
        self.textStartTime=0
        self.savingTime=0
    def getTime(self):
        self.startTime =datetime.datetime.now()
        print('time:', self.startTime)
        

        #self.js.document.getElementById("time").innerHTML=20
        
    def endTime(self):
        self.stopTime =datetime.datetime.now()
        print('end:', self.stopTime)
        self.js.document.getElementById("time").innerHTML=20
    def textInputTime(self):
        self.textStartTime =datetime.datetime.now()
        print('textArea:', self.textStartTime)   
    def savingTimeFunc(self):
        self.savingTime=datetime.datetime.now()
        print('savingTime:', self.savingTime)

@app.route('/')
def index():
    if not os.path.exists(os.path.join(directory,'database' ,'data.db')):
        db.create_all()
    return App.render(render_template('index.html'))
    


@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera, out,thread,start_time, end_time,frame
    if request.method == 'POST':
        user_input = request.form['text']
        if request.form.get('start') == 'Start':
            start_time =datetime.datetime.now()
            print(start_time)
            camera = cv2.VideoCapture(0)
            # Get the width and height of frame
            width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
            height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            file_path=folder_creat()
            out = cv2.VideoWriter(file_path, fourcc, 20.0, (width, height))
            thread = Thread(target = record, args=[out,])
            thread.start()  #Start new thread for recording the video  
        else:
            pass
        if request.form.get('stop') == 'Stop':
            end_time =datetime.datetime.now()
            minutes_dif=end_time-start_time
            duration = divmod(minutes_dif.seconds,60)
            minute,second=duration[0],duration[1]
            camera.release()
            out.release()
            cv2.destroyAllWindows()
        else: pass
        if request.form.get('save') == 'Save':
           
            cam_duration=App.stopTime-App.startTime
            cam_duration=format(cam_duration.total_seconds(),".2f")
            session_duration =App.savingTime-App.textStartTime
            session_duration =format(session_duration.total_seconds(), ".2f")
            table1_input=camera_task(App.startTime,App.stopTime,cam_duration)
            table2_input =operation(App.textStartTime,App.savingTime,session_duration,user_input)
            db.session.add(table1_input)
            db.session.add(table2_input)
            db.session.commit()
           
    elif request.method=='GET':
        return App.render(render_template('index.html'))
    return App.render(render_template('index.html',user_input=user_input))


if __name__ == '__main__':
    app.run(debug=True)