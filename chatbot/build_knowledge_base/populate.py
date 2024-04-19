import os
import json
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv
from tqdm import tqdm
from weaviate.util import generate_uuid5
import weaviate.classes.config as wc

load_dotenv()



def create_movies_collection(client):
    # check if the schema already exists
    if client.collections.exists("Movies"):
        client.collections.delete("Movies")
        print("Deleted the existing 'Movies' schema")

    # Create collection 'Movies'
    client.collections.create(
        name="Movies",
        properties=[
            wc.Property(name="title", data_type=wc.DataType.TEXT),
            wc.Property(name="backdrop_path", data_type=wc.DataType.TEXT),
            wc.Property(name="poster_path", data_type=wc.DataType.TEXT),
            wc.Property(name="overview", data_type=wc.DataType.TEXT),
            wc.Property(name="vote_average", data_type=wc.DataType.NUMBER),
            wc.Property(name="genre_ids", data_type=wc.DataType.INT_ARRAY),
            wc.Property(name="release_date", data_type=wc.DataType.DATE),
            wc.Property(name="popularity", data_type=wc.DataType.NUMBER),
            wc.Property(name="tmdb_id", data_type=wc.DataType.INT),
            wc.Property(name="original_language", data_type=wc.DataType.TEXT),
        ],
        vectorizer_config=wc.Configure.Vectorizer.none(),
    )



def import_movies_data(client):
    """" Import movies data to Weaviate """    
    
    if os.path.exists("/app/build_knowledge_base/datasets/movies_data_1990_2024.csv"):
        df = pd.read_csv("/app/build_knowledge_base/datasets/movies_data_1990_2024.csv")

        embs_url = "/app/build_knowledge_base/datasets/movies_data_1990_2024_embeddings.csv"
        emb_df = pd.read_csv(embs_url)

        movies = client.collections.get("Movies")

        with movies.batch.dynamic() as batch:
            for i, movie in tqdm(enumerate(df.itertuples(index=False)), desc="Importing Movies"):
                release_date = datetime.datetime.strptime(movie.release_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
                genre_ids = json.loads(movie.genre_ids)

                movie_obj = {
                    "title": movie.title,
                    "backdrop_path": movie.backdrop_path,
                    "poster_path": movie.poster_path,
                    "overview": movie.overview,
                    "vote_average": movie.vote_average,
                    "genre_ids": genre_ids,
                    "release_date": release_date,
                    "popularity": movie.popularity,
                    "tmdb_id": movie.id,
                    "original_language": movie.original_language,
                }

                # Get the vector
                vector = emb_df.iloc[i].to_list()

                # add object, vector to batch queue
                batch.add_object(
                    properties=movie_obj,
                    uuid=generate_uuid5(movie.id),
                    vector=vector
                )

        # Check if any objects failed to import
        if len(client.collections.get("Movies").batch.failed_objects) > 0:
            print(f"Failed to import {len(client.collections.get('Movies').batch.failed_objects)} objects")
    else:
        print("File not found: ./datasets/movies_data_1990_2024.csv")



def get_collection_length(client):
    try:
        movies = client.collections.get("Movies")
        return len(list(movies.iterator()))
    except Exception as e:
        raise Exception(f"Could not get collection length: {str(e)}")
