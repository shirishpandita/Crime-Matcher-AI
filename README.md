# 🧠 Crime Pattern Matcher AI  
🌐 **Live App:** [Click here to try it out](https://crime-matcher-ai-giwfu2cgcv7sndfjntesqw.streamlit.app)
An intelligent system to identify and visualize similar crime patterns using natural language input, semantic AI, and geolocation — focused on Jammu & Kashmir.
(⚠️ The map and similarity matching might take up to 1–2 minutes to load depending on internet speed and server response. Please be patient — it's worth the wait! 😊)

---

## 🚀 What It Does

🔍 **Input a crime report**, and it:

- Predicts the **type of crime** using Machine Learning  
- Finds **similar past crimes** using a **semantic similarity model (BERT)**  
- Shows **top 3 most relevant matches**  
- Plots crime locations on a **real-time map**  
- Lets you **download results** as CSV or PDF  

This tool could help in analyzing repetitive crime patterns, improve investigations, and support decision-making.

---

## 🎯 Why I Built This

This project was developed as part of my research interest in AI for forensic science and conflict analysis.  
It’s inspired by real-world crime analysis needs in politically sensitive regions like **Jammu & Kashmir**.  
And yes, I wanted it to be both **technically solid** and **practically useful**.

---

## 🛠️ Features & Tech Stack

| Feature                                      | What It Shows                        |
|---------------------------------------------|--------------------------------------|
| BERT-based Sentence Similarity (MiniLM)     | Understanding of semantic embeddings |
| Crime Category Prediction (ML Classifier)   | Knowledge of supervised ML           |
| Streamlit App UI                            | Front-end deployment skills          |
| Geolocation + Folium Map                    | Data visualization capability        |
| CSV/PDF Export                              | Practical UX enhancements            |
| Feedback-ready Dataset Growth               | Awareness of deployment pipelines    |

---

## 🧩 How It Works (Simple Flow)

1. Load dataset or upload your own
2. Use **BERT** to encode crime reports
3. Use **Logistic Regression** to classify crime type
4. Match your new report to past crimes using **cosine similarity**
5. Show **top 3 matches** with scores and info
6. Predict the most likely crime category
7. Plot crimes on **Folium map**
8. Let you **download** match results

---

## 📁 Project Structure
.
├── app/
|├── crime_matcher_gui.py # Main Streamlit App
│ ├── crime_matcher.py # Core backend logic (if separated)
│ ├── create_dataset.py # Script to generate synthetic dataset
│
├── data/
│ ├── crime_dataset.csv # Your main data
│ └── README.md # Info about data format
│
├── requirements.txt # All dependencies
├── README.md # You're reading it!

---

## 📦 Installation (Run Locally)

```bash
git clone https://github.com/yourusername/crime-pattern-matcher-ai.git
cd crime-pattern-matcher-ai
pip install -r requirements.txt
streamlit run app/crime_matcher_gui.py
```
⚠️ Make sure you’re using Python 3.9 or higher.
🌍 Deploy Online (Optional)  
You can deploy this on:

- Streamlit Cloud – free tier available  
- HuggingFace Spaces  

📜 License  
MIT License. Free to use, modify, and build on.

🙋‍♂️ Maintainer  
Made with ❤️ by **Shirish Pandita**  
Feel free to connect or raise an issue if you want to contribute.
