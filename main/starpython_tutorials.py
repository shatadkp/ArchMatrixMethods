import io
import stardog
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the query
song_lengths_query = """
SELECT ?length WHERE {
  ?song a <http://stardog.com/tutorial/Song> ;
        <http://stardog.com/tutorial/length> ?length .
}
"""

# Execute the query
csv_results = conn.select(song_lengths_query, content_type='text/csv')
df_lengths = pd.read_csv(io.BytesIO(csv_results))

# Convert length to numeric
df_lengths['length'] = pd.to_numeric(df_lengths['length'])

# Plot the distribution
plt.figure(figsize=(10, 6))
sns.histplot(df_lengths['length'], bins=20, kde=True)
plt.title('Distribution of Song Lengths')
plt.xlabel('Length (seconds)')
plt.ylabel('Number of Songs')
plt.show()



###########################3
#####################Number of Tracks per Album

# Define the query
tracks_per_album_query = """
SELECT ?album_name (COUNT(?track) AS ?num_tracks) WHERE {
  ?album a <http://stardog.com/tutorial/Album> ;
         <http://stardog.com/tutorial/name> ?album_name ;
         <http://stardog.com/tutorial/track> ?track .
}
GROUP BY ?album_name
ORDER BY DESC(?num_tracks)
"""

# Execute the query
csv_results = conn.select(tracks_per_album_query, content_type='text/csv')
df_tracks = pd.read_csv(io.BytesIO(csv_results))

# Convert num_tracks to numeric
df_tracks['num_tracks'] = pd.to_numeric(df_tracks['num_tracks'])

# Plot the data
plt.figure(figsize=(12, 8))
sns.barplot(data=df_tracks, x='num_tracks', y='album_name', palette='viridis')
plt.title('Number of Tracks per Album')
plt.xlabel('Number of Tracks')
plt.ylabel('Album Name')
plt.show()



##########################################Number of Albums per Artist

# Define the query
albums_per_artist_query = """
SELECT ?artist_name (COUNT(?album) AS ?num_albums) WHERE {
  ?album a <http://stardog.com/tutorial/Album> ;
         <http://stardog.com/tutorial/artist> ?artist .
  ?artist <http://stardog.com/tutorial/name> ?artist_name .
}
GROUP BY ?artist_name
ORDER BY DESC(?num_albums)
"""

# Execute the query
csv_results = conn.select(albums_per_artist_query, content_type='text/csv')
df_albums_artist = pd.read_csv(io.BytesIO(csv_results))

# Convert num_albums to numeric
df_albums_artist['num_albums'] = pd.to_numeric(df_albums_artist['num_albums'])

# Plot the data
plt.figure(figsize=(12, 6))
sns.barplot(data=df_albums_artist, x='artist_name', y='num_albums', palette='coolwarm')
plt.title('Number of Albums per Artist')
plt.xlabel('Artist Name')
plt.ylabel('Number of Albums')
plt.xticks(rotation=45)
plt.show()



###############################################Number of Albums Released Per Year

# Define the query
albums_per_year_query = """
SELECT ?year (COUNT(?album) AS ?num_albums) WHERE {
  ?album a <http://stardog.com/tutorial/Album> ;
         <http://stardog.com/tutorial/date> ?date .
  BIND(YEAR(?date) AS ?year)
}
GROUP BY ?year
ORDER BY ?year
"""

# Execute the query
csv_results = conn.select(albums_per_year_query, content_type='text/csv')
df_albums_year = pd.read_csv(io.BytesIO(csv_results))

# Convert columns to numeric
df_albums_year['year'] = pd.to_numeric(df_albums_year['year'])
df_albums_year['num_albums'] = pd.to_numeric(df_albums_year['num_albums'])

# Plot the data
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_albums_year, x='year', y='num_albums', marker='o')
plt.title('Number of Albums Released Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Albums')
plt.xticks(df_albums_year['year'], rotation=45)
plt.show()


########################Average Song Length Per Album


# Define the query
avg_song_length_query = """
SELECT ?album_name (AVG(?length) AS ?avg_length) WHERE {
  ?album a <http://stardog.com/tutorial/Album> ;
         <http://stardog.com/tutorial/name> ?album_name ;
         <http://stardog.com/tutorial/track> ?song .
  ?song <http://stardog.com/tutorial/length> ?length .
}
GROUP BY ?album_name
ORDER BY DESC(?avg_length)
"""

# Execute the query
csv_results = conn.select(avg_song_length_query, content_type='text/csv')
df_avg_length = pd.read_csv(io.BytesIO(csv_results))

# Convert avg_length to numeric
df_avg_length['avg_length'] = pd.to_numeric(df_avg_length['avg_length'])

# Plot the data
plt.figure(figsize=(12, 8))
sns.barplot(data=df_avg_length, x='avg_length', y='album_name', palette='magma')
plt.title('Average Song Length Per Album')
plt.xlabel('Average Length (seconds)')
plt.ylabel('Album Name')
plt.show()



####################Total Album Duration


# Define the query
total_album_duration_query = """
SELECT ?album_name (SUM(?length) AS ?total_length) WHERE {
  ?album a <http://stardog.com/tutorial/Album> ;
         <http://stardog.com/tutorial/name> ?album_name ;
         <http://stardog.com/tutorial/track> ?song .
  ?song <http://stardog.com/tutorial/length> ?length .
}
GROUP BY ?album_name
ORDER BY DESC(?total_length)
"""

# Execute the query
csv_results = conn.select(total_album_duration_query, content_type='text/csv')
df_total_duration = pd.read_csv(io.BytesIO(csv_results))

# Convert total_length to numeric
df_total_duration['total_length'] = pd.to_numeric(df_total_duration['total_length'])

# Plot the data
plt.figure(figsize=(12, 8))
sns.barplot(data=df_total_duration, x='total_length', y='album_name', palette='cubehelix')
plt.title('Total Duration of Albums')
plt.xlabel('Total Length (seconds)')
plt.ylabel('Album Name')
plt.show()



#####################3 Top Songwriters by Number of Songs Written

# Define the query
top_songwriters_query = """
SELECT ?writer_name (COUNT(?song) AS ?num_songs) WHERE {
  ?song a <http://stardog.com/tutorial/Song> ;
        <http://stardog.com/tutorial/writer> ?writer .
  ?writer <http://stardog.com/tutorial/name> ?writer_name .
}
GROUP BY ?writer_name
ORDER BY DESC(?num_songs)
LIMIT 10
"""

# Execute the query
csv_results = conn.select(top_songwriters_query, content_type='text/csv')
df_songwriters = pd.read_csv(io.BytesIO(csv_results))

# Convert num_songs to numeric
df_songwriters['num_songs'] = pd.to_numeric(df_songwriters['num_songs'])

# Plot the data
plt.figure(figsize=(12, 6))
sns.barplot(data=df_songwriters, x='num_songs', y='writer_name', palette='Accent')
plt.title('Top 10 Songwriters by Number of Songs Written')
plt.xlabel('Number of Songs')
plt.ylabel('Songwriter Name')
plt.show()



