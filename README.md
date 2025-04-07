# Movie_Recommendation_System

# 🎬 Movie Recommendation System Based on Storyline

## 📌 Project Overview
This project aims to build a **movie recommendation system** that suggests similar movies based on their **storyline (plot summary)**. Using **web scraping** (Selenium), **Natural Language Processing (NLP)**, and **cosine similarity**, the system allows users to input a movie storyline and receive **top 5 recommended movies** from IMDb's 2024 listings. An interactive **Streamlit web app** provides a user-friendly interface.

---

## ✅ Features

- 🎥 Scrape 2024 IMDb movie names and storylines
- 🧹 Clean and preprocess plot summaries
- 📊 Vectorize text using **TF-IDF**
- 🤖 Calculate **cosine similarity** to find storyline-based matches
- 🌐 Interactive **Streamlit app** for real-time recommendations
- 📁 Stores movie data in CSV for easy use and updates

---

## 💼 Business Use Cases

- **Personalized Recommendations**: Suggests movies based on storyline themes and structure.
- **Entertainment Discovery**: Helps users explore new movies similar to their favorite plots.

---

## 🧠 Approach

### 🔍 Data Scraping
- **Source**: IMDb’s 2024 movie list
- **Tools**: Selenium
- **Data Collected**:
  - `Movie Name`
  - `Storyline`
- **Storage**: CSV file for persistent and scalable use

### 🧹 Data Preprocessing
- Remove punctuation, special characters, stopwords
- Tokenization and normalization using **NLTK** or **SpaCy**

### 🔢 Text Representation
- Convert text to numerical form using:
  - **TF-IDF Vectorizer**
  - or **Count Vectorizer**

### 🔗 Cosine Similarity
- Compute similarity between input storyline and each movie's storyline
- Sort movies by similarity scores
- Return **Top 5** most similar movies

---

## 🖥️ Streamlit Web Application

### Features:
- User inputs a short **storyline**
- System displays **top 5 similar movies** with:
  - Movie Name
  - Plot Summary

### Example:
**Input**:
> “A young wizard begins his journey at a magical school where he makes friends and enemies, facing dark forces along the way.”

**Output**:
- *The Wizard’s Journey*: A boy discovers his magical abilities and faces a powerful sorcerer.
- *The Magic Academy*: A student navigates life at a school for magic, facing powerful challenges.
- *The Dark Sorcerer*: A young hero confronts an ancient threat to the magical world.
- ...

---

## 📃 License
MIT License. Free for personal and academic use.

---

## 👨‍💻 Authors
- **Rajeshwari Arumugam** – AI/ML Developer
