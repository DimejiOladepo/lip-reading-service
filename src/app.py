from flask import Flask,render_template,Response,request
import cv2
import os
import datetime as datetime,time
from threading import Thread

app = Flask(__name__, template_folder='./templates')
global camera,switch, rec_frame,start_time,end_time,frame
camera = None
switch =0
frame =None


def record(out):
    global rec_frame, frame
    rec_frame =frame
    while True:
        time.sleep(0.05)
        out.write(rec_frame)


def getAviNameWithDate(nameIn="output_video.avi"):
    """Needs a file ending on .avi, inserts _<date> before .avi. """

    if not nameIn.endswith(".avi"):
        raise ValueError("filename must end on .avi")
    filename = nameIn.replace(".avi","_{0}.avi").format(datetime.datetime.now().strftime("%Y-%m-%d"))
    return filename


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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera, out,thread,start_time, end_time,frame
    if request.method == 'POST':
        if request.form.get('start') == 'Start':
            start_time =datetime.datetime.now()
            print(start_time)
            camera = cv2.VideoCapture(0)
            # Get the width and height of frame
            width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
            height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            file_path=os.path.normpath(os.getcwd() + os.sep + os.pardir+'/video/output.mp4')
            out = cv2.VideoWriter(file_path, fourcc, 20.0, (width, height))
            thread = Thread(target = record, args=[out,])
            thread.start()  #Start new thread for recording the video  
        else:
            pass
        if request.form.get('stop') == 'Stop':
            end_time =datetime.datetime.now()
            print(end_time)
            minutes_dif=end_time-start_time
            duration = divmod(minutes_dif.seconds,60)
            minute,second=duration[0],duration[1]
            print(duration)
            camera.release()
            out.release()
            cv2.destroyAllWindows()
        else: pass
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html',test ='testing')


if __name__ == '__main__':
    app.run(debug=True)