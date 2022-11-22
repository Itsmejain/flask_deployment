from flask import Flask, flash,jsonify, redirect, render_template, request, url_for
import pandas as pd
import numpy as np
import math
from datetime import datetime


app = Flask(__name__, 
            template_folder="./templates")


@app.route("/")
def home():
 return render_template('index.html')

@app.route('/findminmax',methods=['GET','POST'])
def findminmax():
    text = ""
    if request.method == 'POST':
      requestdata = request.data.decode('UTF-8')
      requestdatalist = requestdata.split("||")
      nameofstock = requestdatalist[0]
      datestart = requestdatalist[1]
      dateend = requestdatalist[2]




    csvname = "archive/"+nameofstock+".csv"


    df = pd.read_csv(csvname)


    if datestart != "" and dateend == "":
        dateend = datetime.strptime(datestart, '%Y-%m-%d').date() + pd.DateOffset(years=1)
        dateend = dateend.strftime('%Y-%m-%d')

    elif datestart == "" and dateend != "":
        datestart = datetime.strptime(dateend, '%Y-%m-%d').date() + pd.DateOffset(years=-1)
        datestart = datestart.strftime('%Y-%m-%d')


    elif datestart == "" and dateend=="":
        datestart = str(df.iloc[0]['Date'])
        dateend = str(df.iloc[-1]['Date'])


    df1 = df[df['Date'].between(datestart,dateend)]
    alltimehigh = df1.High.max()
    alltimelow = df1.Low.min()


    if(math.isnan(alltimehigh)):
        alltimehigh = "NO DATA"
    
    if(math.isnan(alltimelow)):
        alltimelow = "NO DATA"
    
    text = nameofstock +"\nHighest Value of Stock :"+str(alltimehigh)+"\nLowest Value of Stock :" +str(alltimelow)
    return text

if __name__ == "__main__":
 app.run(debug=True,port=8000)


