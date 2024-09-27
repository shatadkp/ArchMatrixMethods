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
