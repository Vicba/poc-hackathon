import requests
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HUGGINGFACE_APIKEY")

def query(texts):
    model_id = "sentence-transformers/all-MiniLM-L6-v2"

    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}

    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
    )
    return response.json()


# df = pd.read_csv("./datasets/circuits.csv")
df = pd.read_csv("./merged_data.csv")
df = df[['position', 'points', 'laps', 'rank', 'year', 'name_x', 'name_y', 'location', 'country', 'forename', 'surname', 'nationality_x', 'name', 'status']]
df = df.head(100)
print(df.head())

# Loop through the dataset to generate vectors in batches
emb_dfs = list()
src_texts = list()
for i, row in enumerate(df.itertuples(index=False)):
    # association between these embeddings and other properties of the movies is maintained through the indexing of the resulting DataFrame. 
    # so only the title and overview will be used for semantic similarity

    # resultId,raceId,driverId,constructorId,number_x,grid,position,positionText,positionOrder,points,laps,time_x,milliseconds,fastestLap,rank,fastestLapTime,fastestLapSpeed,statusId,year,round,circuitId,name_x,date,time_y,url_x,fp1_date,fp1_time,fp2_date,fp2_time,fp3_date,fp3_time,quali_date,quali_time,sprint_date,sprint_time,circuitRef,name_y,location,country,lat,lng,alt,url_y,driverRef,number_y,code,forename,surname,dob,nationality_x,url,name,nationality_y,status

    # src_text = f"Circuit reference: {row.circuitRef} Name: {row.name} Location: {row.location} Country: {row.country}, Altitude: {row.alt} Lat: {row.lat} Lng: {row.lng} URL: {row.url}"
    
    src_text = f"Position: {row.position} Points: {row.points} Laps: {row.laps} Rank: {row.rank} Year: {row.year} Name_x: {row.name_x} Name_y: {row.name_y} Location: {row.location} Country: {row.country} Forename: {row.forename} Surname: {row.surname} Nationality_x: {row.nationality_x} Name: {row.name} Status: {row.status}"
    print(src_text)

    # Add to the buffer
    src_texts.append(src_text)
    if (len(src_texts) == 1000) or (i + 1 == len(df)):  # Get embeddings in batches of 50
        # Get a batch of embeddings
        output = query(src_texts)
        emb_df = pd.DataFrame(output, index=src_texts)
        # Add the batch of embeddings to a list
        emb_dfs.append(emb_df)
        # Reset the buffer
        src_texts = list()


emb_df = pd.concat(emb_dfs)
emb_df.to_csv(
    f"./datasets/embeddings/merged_data.csv",
    index=False,
)