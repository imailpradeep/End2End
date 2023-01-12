import pymongo, os, json
import pandas as pd

def upload_data_to_mongoDB():
    client = pymongo.MongoClient("mongodb+srv://imailpradeep:ammaacha@cluster0.gujy4jv.mongodb.net/test")

    DATABASE_NAME="MachineLearning"

    if __name__=="__main__":
        directory_path = "/config/workspace/market_basket"
        file_list = os.listdir(directory_path)
            
        # for checking
        #file_list = file_list[0:2]
        # upload each file in the mongoDB collection
        for file in file_list:
            df = pd.read_csv(os.path.join(directory_path,file))
            print(f"Rows and columns: {df.shape}")

            #Convert dataframe to json so that we can dump these record in mongo db
            df.reset_index(drop=True,inplace=True)    # to remove the first column in dataframe
            json_record = list(json.loads(df.T.to_json()).values())

            #insert converted json record to mongo db
            client[DATABASE_NAME][file].insert_many(json_record)

            
upload_data_to_mongoDB()