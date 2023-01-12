import pymongo,os, json, sys
import pandas as pd
from logger import logging
from exception import ecommerce_exception


MongoURL = os.getenv("MONGO_DB_URL")

def upload_data_to_mongoDB():
    """ uploads data to mondoDB from the market_basket folder"""
    # Provide the mongodb localhost url to connect python to mongodb.
    try:
        client = pymongo.MongoClient(MongoURL)
    except Exception as e:
        raise ecommerce_exception(e, sys) 


    DATABASE_NAME="MachineLearning"

    if __name__=="__main__":
        try:
        # get the names of all the files in the data folder 
            directory_path = "/config/workspace/market_basket"
            file_list = os.listdir(directory_path)
            
            # for checking
            #file_list = file_list[0:2]
            # upload each file in the mongoDB collection
            for file in file_list:
                logging.info(f"starting data dump from {directory_path}/{file} to mongo DB")
                df = pd.read_csv(os.path.join(directory_path,file))
                print(f"Rows and columns: {df.shape}")

                #Convert dataframe to json so that we can dump these record in mongo db
                df.reset_index(drop=True,inplace=True)    # to remove the first column in dataframe
                json_record = list(json.loads(df.T.to_json()).values())

                #insert converted json record to mongo db
                client[DATABASE_NAME][file].insert_many(json_record)
                logging.info(f"completed data dump from folder to mongoDB DataBase- {DATABASE_NAME} collection- {file}")
            
        except Exception as e:
            raise ecommerce_exception(e, sys)   
