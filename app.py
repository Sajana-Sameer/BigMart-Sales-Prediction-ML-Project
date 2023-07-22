from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            Item_Weight=float(request.form.get('item_weight')),
            Item_Fat_Content=request.form.get('item_fat_content'),
            Item_Visibility=float(request.form.get('item_visibility')),
            Item_Type=request.form.get('item_type'),
            Item_MRP=float(request.form.get('item_mrp')),
            Outlet_Establishment_Year=int(request.form.get('outlet_establishment_year')),
            Outlet_Size=int(request.form.get('outlet_size')),
            Outlet_Location_Type=int(request.form.get('outlet_location_type')),
            Outlet_Type=int(request.form.get('outlet_type'))
#            outlet_size=float(request.form.get('Outlet_Size'))

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=round(results[0], 2))
    

if __name__=="__main__":
    app.run(host="0.0.0.0")     