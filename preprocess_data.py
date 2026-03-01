import pandas as pd
import numpy as np

def clean_data(file_path):
    df = pd.read_csv(file_path)

    df.replace(['', ' ', 'NA', 'None'], np.nan, inplace=True)

    
    if 'User Id' in df.columns:
        df['User Id'] = pd.to_numeric(df['User Id'], errors='coerce')

    if 'ProdID' in df.columns:
        df['ProdID'] = pd.to_numeric(df['ProdID'], errors='coerce')

    
    if 'User Id' in df.columns and 'ProdID' in df.columns:
        df.dropna(subset=['User Id', 'ProdID'], inplace=True)
        df = df[(df['User Id'] != 0) & (df['ProdID'] != 0)]

  
    text_cols = df.select_dtypes(include='object').columns
    df[text_cols] = df[text_cols].fillna('')

    # Clean ImageURL
    if 'ImageURL' in df.columns:
        df['ImageURL'] = df['ImageURL'].str.replace('|', '', regex=False)

    df.reset_index(drop=True, inplace=True)

    return df


if __name__ == "__main__":
    cleaned_df = clean_data("clean_data.csv")
    print(cleaned_df.head())
    cleaned_df.to_csv("cleaned_output.csv", index=False)