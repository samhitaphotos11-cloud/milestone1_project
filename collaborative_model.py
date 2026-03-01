import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.read_csv("cleaned_output.csv")

print("Columns:", ratings.columns.tolist())

user_col = [c for c in ratings.columns if "user" in c.lower()][0]
item_col = [c for c in ratings.columns if "name" in c.lower() or "product" in c.lower()][0]
rating_col = [c for c in ratings.columns if "rating" in c.lower()][0]

user_item = ratings.pivot_table(
    index=user_col,
    columns=item_col,
    values=rating_col
).fillna(0)

print("Matrix shape:", user_item.shape)

item_similarity = cosine_similarity(user_item.T)
item_names = user_item.columns.tolist()

def recommend(product_name, top_n=5):
    if product_name not in item_names:
        return "Product not found"
    
    idx = item_names.index(product_name)
    scores = list(enumerate(item_similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    indices = [i[0] for i in scores]
    return [item_names[i] for i in indices]
print("Items:", len(item_names))
if __name__ == "__main__":
    print("Sample recommendations:\n")
    print(recommend(item_names[0]))