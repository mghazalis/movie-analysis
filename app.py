import pandas as pd
import matplotlib.pyplot as plt

# Load movie and rating data from Parquet files
movies_df = pd.read_parquet("movie.parquet")
ratings_df = pd.read_parquet("rating.parquet")

# Create a bar chart for the top 10 movies by average rating
merged_df = pd.merge(ratings_df, movies_df, on='movieId')
top_10_movies = merged_df.groupby('title')['rating'].mean().nlargest(10)
plt.figure(figsize=(10, 6))
plt.barh(top_10_movies.index, top_10_movies.values, color='skyblue')
plt.xlabel('Average Rating')
plt.ylabel('Movie Title')
plt.title('Top 10 Movies by Average Rating')
plt.gca().invert_yaxis()
plt.show()

# Create a pie chart for movie genres market share
genre_market_share = movies_df['genres'].str.get_dummies(sep='|').sum() / len(movies_df) * 100
plt.figure(figsize=(8, 8))
plt.pie(genre_market_share.values, labels=genre_market_share.index, autopct='%1.1f%%', startangle=140)
plt.title('Movie Genres Market Share')
plt.axis('equal')
plt.show()
