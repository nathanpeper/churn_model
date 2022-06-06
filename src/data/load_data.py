import yaml
import argparse
import numpy as np 
import pandas as pd 
import zipfile

def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def unzip_data(zip_data_path, unzip_data_path):
    """
    unzip csv dataset from given path
    input: external zipped data path 
    output:unzipped data in path 
    """
    with zipfile.ZipFile(zip_data_path,"r") as zip_ref:
        zip_ref.extractall(unzip_data_path)
    

def load_data(data_path,model_var):
    """
    load csv dataset from given path
    input: csv path 
    output:pandas dataframe 
    note: Only 6 variables are used in this model building stage for the simplicity.
    """
    df = pd.read_csv(data_path, sep=",", encoding='utf-8')
    df=df[model_var]
    return df

def load_raw_data(config_path):
    """
    load data from external location(data/external) to the raw folder(data/raw) with train and teting dataset 
    input: config_path 
    output: save train file in data/raw folder 
    """
    config=read_params(config_path)
    external_data_path=config["external_data_config"]["external_data_csv"]
    raw_data_path=config["raw_data_config"]["raw_data_path"]
    raw_data_csv=config["raw_data_config"]["raw_data_csv"]
    interim_data_path=config["interim_data_config"]["interim_data_csv"]
    model_var=config["interim_data_config"]["model_var"]
    
    unzip_data(external_data_path, raw_data_path)
    df=load_data(raw_data_csv,model_var)
    df.to_csv(interim_data_path,index=False)
    
if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_raw_data(config_path=parsed_args.config)
