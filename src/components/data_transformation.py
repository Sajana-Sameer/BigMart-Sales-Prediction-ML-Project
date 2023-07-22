import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.preprocessing import LabelEncoder
#import category_encoders as ce
from sklearn.base import BaseEstimator, TransformerMixin
from statistics import mode

#from src.components.data_ingestion import DataIngestion

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataCleaner:
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def clean_data(self, X):
        # Filling missing values in Item_Weight based on Item_Identifier and Item_Type
        logging.info("Entering cleaning data")
               
        X['Item_Weight'].fillna(X.groupby('Item_Identifier')['Item_Weight'].transform('median'), inplace=True)
        X['Item_Weight'].fillna(X.groupby('Item_Type')['Item_Weight'].transform('median'), inplace=True)
        
        # Filling missing values in Item_Visibility based on Item_Identifier and Outlet_Type
        X['Item_Visibility'].fillna(X.groupby(['Item_Identifier', 'Outlet_Type'])['Item_Visibility'].transform('median'), inplace=True)
        X['Item_Visibility'].fillna(X.groupby(['Item_Type', 'Outlet_Type'])['Item_Visibility'].transform('median'), inplace=True)
        logging.info("Entering categorical cleaning data")
      #  print(X.head(10))
        X['Outlet_Size'] = X.groupby('Outlet_Type')['Outlet_Size'].transform(lambda x: x.fillna(mode(x)))

      #  X['Item_Category']=X['Item_Identifier'].str[:2].map({'FD' : 'Food','NC' : 'Non-Consumable','DR' : 'Drinks'})
        X['Item_Fat_Content'] =X['Item_Fat_Content'].replace({ 'LF' : 'Low Fat','reg' : 'Regular','low fat' : 'Low Fat'})
        X.loc[X['Item_Identifier'].str[:2] =="NC",'Item_Fat_Content'] = "Non-Edible"
        logging.info(" categorical values cleaned")  
    
        logging.info("Entering LAbel Encode data")
        columns_to_encode = ['Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
        label_encoder = LabelEncoder()
        X[columns_to_encode] = X[columns_to_encode].apply(lambda x: label_encoder.fit_transform(x))
        return X
    
    def drop_unwanted_features(self, X):
        # Drop unwanted features from the DataFrame
        X = X.drop(['Item_Identifier', 'Outlet_Identifier'], axis='columns')
        logging.info(f"deleted")

        return X


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function si responsible for data trnasformation
        
        '''
        try:
            
            
            logging.info("Entering the get_data_transformer_object")
            numerical_columns = ["Item_Weight", "Item_Visibility","Item_MRP","Outlet_Establishment_Year","Outlet_Size",
                                 "Outlet_Location_Type","Outlet_Type"]
            categorical_columns = [
                "Item_Fat_Content",
                "Item_Type",
            ]
            
        
            # Data cleaning step
            cleaner = DataCleaner()
            
       
            # Missing values
            num_pipeline= Pipeline(
                steps=[
#                ("cleaner", cleaner),  # Data cleaning step
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                #("label_encode", LabelEncoderTransformer(columns=['Item_Fat_Content', 'Item_Category', 'Item_Type'])),
               

                ("one_hot_encode", OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
            
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]
            )
            logging.info("PReprocessor")
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
        
            cleaner = DataCleaner()
            train_df=cleaner.clean_data(train_df)
            test_df=cleaner.clean_data(test_df)
            
            train_df[['Item_Fat_Content', 'Item_Type']] = train_df[['Item_Fat_Content',  'Item_Type']].astype(str)
            test_df[['Item_Fat_Content',  'Item_Type']] = test_df[['Item_Fat_Content',  'Item_Type']].astype(str)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            print("Data types")
            print(train_df.dtypes)           
            target_column_name="Item_Outlet_Sales"
            #numerical_coclumns = ["writing_score", "reading_score"]
            drop_columns=["Item_Outlet_Sales","Item_Identifier","Outlet_Identifier"]
            input_feature_train_df=train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]
            logging.info("Droping Target variable")
            logging.info(
                f"Applrying preprocessing object on training dataframe and testing dataframe."
            )#  
            print("\n\n")        
            
            preprocessing_obj=self.get_data_transformer_object()

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
             # Apply the drop_unwanted_features function to remove the unwanted columns
        #    input_feature_train_arr = cleaner.drop_unwanted_features(input_feature_train_arr)
        #    input_feature_test_arr = cleaner.drop_unwanted_features(input_feature_test_arr)
        #    logging.info("Deleted unwanted features")

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
        
