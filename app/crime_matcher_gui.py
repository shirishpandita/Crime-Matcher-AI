from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import time
from io import BytesIO
import base64
from fpdf import FPDF

def convert_df_to_csv(data):
    df_export = pd.DataFrame(data)
    return df_export.to_csv(index=False).encode('utf-8')
def convert_to_pdf(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Top Crime Matches")
    y -= 30
    c.setFont("Helvetica", 10)

    for match in data:
        lines = [
            f"Match Score: {match['score']:.2f}",
            f"ID: {match['id']}",
            f"Location: {match['location']}",
            f"Time: {match['time']}",
            f"Type: {match['crime_type']}",
            f"Description: {match['description']}",
            "-" * 60
        ]
        for line in lines:
            if y < 50:
                c.showPage()
                y = height - 40
                c.setFont("Helvetica", 10)
            c.drawString(50, y, line)
            y -= 15

    c.save()
    buffer.seek(0)
    return buffer
@st.cache_data
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="crime_mapper", timeout=10)
    location = geolocator.geocode(f"{location_name}, Jammu and Kashmir, India")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def add_coordinates(df):
    latitudes = []
    longitudes = []
    for loc in df['location']:
        lat, lon = get_coordinates(loc)
        time.sleep(1.2)
        latitudes.append(lat)
        longitudes.append(lon)
    df['latitude'] = latitudes
    df['longitude'] = longitudes
    return df

# Load the crime dataset
# 📂 CSV Upload Section
st.sidebar.header("📂 Upload Crime Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='cp1252')
    st.sidebar.success("✅ Dataset uploaded successfully!")
else:
    df = pd.read_csv("crime_dataset.csv", encoding='cp1252')
    st.sidebar.info("Using default dataset.")

# 🧠 Only run geocoding if coordinates are missing
if 'latitude' not in df.columns or df['latitude'].isnull().any():
    df = add_coordinates(df)
    df.to_csv("crime_dataset.csv", index=False, encoding='cp1252')  # Save coordinates permanently
df["text"] = df["location"] + " " + df["weapon"] + " " + df["time"] + " " + df["description"]

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
vectors = model.encode(df["text"].tolist(), convert_to_tensor=True)

# ----------------- Classification Model -----------------
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(max_iter=1000)
clf.fit(vectors, df["crime_type"])  # Train the classifier

# Train classifier to predict crime_type
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["crime_type"], test_size=0.2, random_state=42)
clf_vectorizer = TfidfVectorizer()
X_train_vec = clf_vectorizer.fit_transform(X_train)
X_test_vec = clf_vectorizer.transform(X_test)

classifier = LogisticRegression()
classifier.fit(X_train_vec, y_train)

# Optional evaluation report
y_pred = classifier.predict(X_test_vec)
classification_metrics = classification_report(y_test, y_pred, output_dict=True)
if st.sidebar.checkbox("📊 Show Model Metrics"):
    st.sidebar.subheader("Classification Report")
    st.sidebar.write(pd.DataFrame(classification_metrics).T)

# Streamlit UI
st.title("🧠 Crime Pattern Matcher AI")
st.markdown("Enter a new crime report to find similar past cases.")

# Optional reset button to clear previous results
if st.button("🧼 Reset"):
    st.session_state.match_results = None

# User input form
location = st.text_input("📍 Location")
weapon = st.text_input("🔪 Weapon Used")
time = st.selectbox("🕰️ Time of Day", ["day", "night"])
description = st.text_area("📝 Description of Crime")

if "match_results" not in st.session_state:
    st.session_state.match_results = None

if st.button("🔍 Find Similar Cases"):
    if location and weapon and time and description:
        new_text = location + " " + weapon + " " + time + " " + description
        # Predict crime type for the input
        pred_vector = clf_vectorizer.transform([new_text])
        predicted_crime = classifier.predict(pred_vector)[0]
        st.success(f"🧠 Predicted Crime Type: **{predicted_crime}**")


        # Similarity calculation
        from sentence_transformers.util import cos_sim
        new_vector = model.encode([new_text], convert_to_tensor=True)
        similarities = cos_sim(new_vector, vectors)[0]
        scores = list(enumerate(similarities.cpu().numpy()))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        # Store top 3 matches
        st.session_state.match_results = [
            {
                "score": score,
                "id": df.iloc[idx]['id'],
                "location": df.iloc[idx]['location'],
                "time": df.iloc[idx]['time'],
                "crime_type": df.iloc[idx]['crime_type'],
                "description": df.iloc[idx]['description']
            }
            for idx, score in sorted_scores[:3]
        ]
        predicted_crime_type = clf.predict(new_vector)[0]
        st.success(f"🧠 Predicted Crime Type: **{predicted_crime_type}**")

    else:
        st.warning("Fill all fields before clicking the button.")

# 🔁 Show stored results if they exist
if st.session_state.match_results:
    st.subheader("Top Matches:")

    # Convert to CSV
    csv_data = convert_df_to_csv(st.session_state.match_results)
    st.download_button(
        label="📄 Download Matches as CSV",
        data=csv_data,
        file_name="crime_matches.csv",
        mime="text/csv"
    )

    # Show each match
    for match in st.session_state.match_results:
        st.markdown(f"""
        **Match Score:** `{match['score']:.2f}`  
        **ID:** {match['id']}  
        **Location:** {match['location']}  
        **Time:** {match['time']}  
        **Type:** {match['crime_type']}  
        **Description:** {match['description']}  
        ---
        """)

# ---------------- Map Section ----------------
st.subheader("📍 Crime Map of Jammu & Kashmir")
map_df = df.dropna(subset=['latitude', 'longitude'])

m = folium.Map(location=[33.7782, 76.5762], zoom_start=7)

for _, row in map_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"<b>{row['location']}</b><br>{row['description']}<br>Type: {row['crime_type']}",
        tooltip=row['location'],
        icon=folium.Icon(color='red' if row['crime_type'] == 'murder' else 'blue')
    ).add_to(m)

st_data = st_folium(m, width=700, height=500)
