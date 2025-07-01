import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your dataset
df = pd.read_csv("crime_dataset.csv")

# Combine key text fields for analysis
df["text"] = df["location"] + " " + df["weapon"] + " " + df["time"] + " " + df["description"]

# Vectorize the text
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(df["text"])

# 👇 Enter your new crime report here
new_case = {
    "location": "Srinagar",
    "weapon": "knife",
    "time": "night",
    "description": "A man was attacked with a knife near his home during the night."
}

# Prepare the new case for vectorization
new_text = new_case["location"] + " " + new_case["weapon"] + " " + new_case["time"] + " " + new_case["description"]
new_vector = vectorizer.transform([new_text])

# Compute cosine similarity
similarities = cosine_similarity(new_vector, vectors)

# Get top 3 similar cases
scores = list(enumerate(similarities[0]))
sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

# Print results
print("\n🔍 Top Matching Cases:\n")
for idx, score in sorted_scores[:3]:
    match = df.iloc[idx]
    print(f"🔥 Match Score: {score:.2f}")
    print(f"🆔 ID: {match['id']}")
    print(f"📍 Location: {match['location']}")
    print(f"🕰️ Time: {match['time']}")
    print(f"🧠 Crime Type: {match['crime_type']}")
    print(f"📄 Description: {match['description']}")
    print("-" * 40)
