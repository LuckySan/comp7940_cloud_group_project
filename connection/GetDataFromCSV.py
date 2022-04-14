import pandas as pd 



def readRecipeData(): 
    df = pd.read_csv("./data/full_dataset_sample.csv")
    return df

