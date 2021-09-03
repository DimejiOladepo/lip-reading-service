from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np


app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
