import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load cleaned dataset
data = pd.read_csv("clean_data.csv")

# Ensure Tags column exists
data["Tags"] = data["Tags"].fillna("")

# TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(data["Tags"])

# Cosine similarity matrix
similarity = cosine_similarity(tfidf_matrix)

def recommend(product_name, top_n=5):
    if product_name not in data["Name"].values:
        return "Product not found"

    idx = data[data["Name"] == product_name].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    indices = [i[0] for i in scores]
    return data["Name"].iloc[indices]

# Example test
if __name__ == "__main__":
    print(recommend(data["Name"].iloc[0]))