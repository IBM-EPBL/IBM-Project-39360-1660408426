# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 00:07:14 2022

@author: HP
"""

from flask import Flask,render_template,request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests

app = Flask(__name__,template_folder="templates") 

model=load_model('nutrition.h5')
print("Loaded model from disk")

@ app.route('/')
def home():
    return render_template('home.html') 

@ app.route('/image1', methods=['GET', 'POST']) 
def image1():
    return render_template("image.html")


@ app.route('/predict' ,methods=['GET','POST']) 
def lanuch():
    if request.method=='POST':
        f=request.files['file'] 
        basepath=os.path.dirname('__file__') 
        filepath=os.path.join(basepath,"uploads",f.filename)
        f.save(filepath) 
        
        img=image.load_img(filepath,target_size=(64,64)) 
        x=image.img_to_array(img) 
        x=np.expand_dims(x,axis=0) 
        
        pred=np.argmax(model.predict(x), axis=1)
        print("prediction",pred) 
        index=['APPLE','BANANA','ORANGE','PINEAPPLE','WATERMELON']
        
        result=str(index[pred[0]])
        print(result)
        x=result
        result=nutrition(result)
        print(result)
        
        return render_template("0.html",showcase=(result),showcase1=(x))
def nutrition(index):
    
    import requests

    url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"

    querystring = {"query":index}

    headers = {
	"X-RapidAPI-Key": "85887549f4msh51e7315b280a87ep1f43e0jsn585c940f2ea6",
	"X-RapidAPI-Host": "calorieninjas.p.rapidapi.com"
     }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return response.json()['items']
if __name__ == "__main__":
    app.run(debug=False) 
       