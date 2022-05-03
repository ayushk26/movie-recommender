import numpy as np
import pandas as pd
import math

df = pd.read_csv('ratings_small.csv')
df = pd.DataFrame(df)
df = df.drop_duplicates()

movie_data = {}

for i in range(len(df["userId"])):
    if df["movieId"][i] not in movie_data.keys():
        movie_data[df["movieId"][i]] = np.zeros(len(df.userId.unique()))         
        movie_data[df["movieId"][i]][df["userId"][i]-1] = df["rating"][i]
    else:
        movie_data[df["movieId"][i]][df["userId"][i]-1] = df["rating"][i]

def get_rating(user,movieId,df,movie_data):
    nearest_neighbors = 10
    movieId = movieId
    simmilarity_factor = []

    for i in movie_data.keys():
        val = movie_data[movieId].dot(movie_data[i])/(np.linalg.norm(movie_data[movieId])*np.linalg.norm(movie_data[i]))
        simmilarity_factor.append({"movie":i,"simmilarity":val})

    ordered_simmilarity_factor = sorted(simmilarity_factor,key = lambda i:i["simmilarity"],reverse = True ) 
    nearest_neighbor_movies = ordered_simmilarity_factor[1:1+nearest_neighbors]
    user_ID = user

    new_df = df.query('userId =='+str(user_ID))

    total_simmilarity = 0
    rating = 0
    for i in nearest_neighbor_movies:
        previous_rating = new_df.query('movieId =='+str(i["movie"]))["rating"]
        if len(previous_rating) == 0:
            previous_rating = 0
        else:
            previous_rating = previous_rating
        rating += i["simmilarity"]*previous_rating
        total_simmilarity += i["simmilarity"]
    rating = rating/total_simmilarity
    return float(rating)

def recommend_movies(user,df,movie_data):
    progress = 0
    ratings = []
    all_movies = df["movieId"]
    user_watched_movies = df.query("userId =="+str(user))["movieId"]
    for current_movie in all_movies[:1000]:
        if current_movie not in user_watched_movies:
            rating = get_rating(user,current_movie,df,movie_data)
            progress +=1
            if not math.isnan(rating):
                ratings.append({"movieId":current_movie,"rating":rating})
                print(str(((progress+1)/(len(all_movies)-len(user_watched_movies)))*100)+"%")
    ratings = sorted(ratings, key = lambda i:i["rating"],reverse=True)
    return ratings[0:10]

print(recommend_movies(5,df,movie_data))

