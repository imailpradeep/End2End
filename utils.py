import pandas as pd
from logger import logging
from exception import ecommerce_exception
import os,sys, pymongo
from pymongo import MongoClient

# Connect to the MongoDB server
# Provide the mongodb localhost url to connect python to mongodb.
# collect the tables into separate dataframes

def get_data_from_MongoDB(): 
    """ collects data from mongoDB and combines all the data into df_list file""" 
    try:
        client = pymongo.MongoClient("mongodb+srv://imailpradeep:ammaacha@cluster0.gujy4jv.mongodb.net/test")
        logging.info("connected to MongoDB")
    except Exception as e:
        raise ecommerce_exception(e, sys) 

    # Get the database
    try: 
        db = client['MachineLearning']
        # Get the list of collections
        collections = db.list_collection_names()
        # Print the list of collections
        #print(collections)
        # Get data from the collections
        df_list = [] # to store df
        df_names_list = []
        for file in collections:
            logging.info(f"Reading data from database: MachineLearning and collection: {file}")
            df_name = 'df_' + file # get individual names
            df_names_list.append(df_name)
            df_name = pd.DataFrame(list(client['MachineLearning'][file].find()))
            logging.info(f"Found columns: {df_name.columns}")
                
            if "_id" in df_name.columns: # drop the id column
                logging.info(f"Dropping column: _id ")
                df_name = df_name.drop("_id",axis=1)
            
            df_list.append(df_name)
        logging.info(f"The dataframes have been obtained as a list in df_list ")
        logging.info(f"The names of files produced are : {df_names_list}")
        print(df_names_list)
        return df_list
    except Exception as e:
        raise ecommerce_exception(e, sys) 
    
"""
def join_df(df_list):
    final_df = pd.DataFrame()
    for i in range(len(df_list)):
        final_df = pd.merge(final_df,df_list[i],how = 'inner')
    return final_df

#final_df = join_df(df_list)


"""