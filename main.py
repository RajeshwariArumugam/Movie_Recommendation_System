import pandas as pd
import numpy as np
import re
import streamlit as st
import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Function to preprocess text (lemmatization + stopword removal)
def preprocess_text(text):
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters, numbers, extra spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Lemmatization & stopword removal
    doc = nlp(text)
    words = [token.lemma_ for token in doc if not token.is_stop and len(token.text) > 2]
    
    return ' '.join(words)

# Function to clean movie titles (remove numbering)
def clean_title(title):
    if pd.isna(title):
        return ""
    return re.sub(r'^\d+\.\s*', '', title).strip()

# Function to get movie recommendations using Sentence Transformers
def get_recommendations(user_input, df, model, embeddings):
    # Preprocess user input
    processed_input = preprocess_text(user_input)
    
    # Convert to embedding
    user_embedding = model.encode(processed_input, convert_to_tensor=True)
    
    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(user_embedding, embeddings)[0].cpu().numpy()
    
    # Get similarity scores
    sim_scores = list(enumerate(similarities))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Filter results based on similarity threshold (avoid irrelevant results)
    top_indices = [i[0] for i in sim_scores if i[1] > 0.3][:10]  # Get more movies to ensure diversity
    
    # Get unique top recommendations
    recommendations = df.iloc[top_indices].drop_duplicates(subset=['title'])
    
    # Exclude the movie entered by the user
    user_input_title = df[df['storyline'].str.lower() == user_input.lower()]['title'].values
    if len(user_input_title) > 0:
        recommendations = recommendations[recommendations['title'].str.lower() != user_input_title[0].lower()]
    
    return recommendations.head(5)  # Return top 5 recommendations

# Main Streamlit app
def main():
    st.title("Movie Recommendation System Based on Storyline")
    st.write("Enter a movie plot or storyline to get similar movie recommendations")
    
    try:
        df = pd.read_csv("imdb_movies.csv")
        
        # Clean column names
        df.columns = [col.lower() for col in df.columns]
        
        # Clean titles
        df['title'] = df['title'].apply(clean_title)
        
        # Drop missing storylines
        df = df.dropna(subset=['storyline'])
        
        # Preprocess storylines
        with st.spinner("Processing movie descriptions..."):
            df['processed_storyline'] = df['storyline'].apply(preprocess_text)
        
        # Load Sentence Transformer model
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Convert all storylines into embeddings
        embeddings = model.encode(df['processed_storyline'].tolist(), convert_to_tensor=True)
        
        st.success("Preprocessing complete! Ready for recommendations.")
        
        # User input
        user_input = st.text_area("Enter a movie plot or storyline:", "")
        
        if st.button("Get Recommendations"):
            if user_input:
                # Get recommendations
                recommendations = get_recommendations(user_input, df, model, embeddings)
                
                # Display recommendations
                st.subheader("Top 5 Movie Recommendations:")
                
                for i, (_, row) in enumerate(recommendations.iterrows(), 1):
                    st.markdown(f"**{i}. {row['title']}**")
                    with st.expander("Show Storyline"):
                        st.write(row['storyline'])
                    st.markdown("---")
            else:
                st.warning("Please enter a storyline to get recommendations.")
    
    except FileNotFoundError:
        st.error("Error: 'imdb_movies_by_genre.csv' file not found. Please check the file path.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
