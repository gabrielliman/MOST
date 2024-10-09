import re
import numpy as np
import sentence_embedding  # Import C++ class
from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify, render_template
from typing import List, Dict, Any

app = Flask(__name__)

# Initialize the SentenceTransformer model outside of the route
model: SentenceTransformer = SentenceTransformer("all-mpnet-base-v2")

def text_to_sentence(text: str) -> List[str]:
    """
    Splits the input text into sentences.
    
    Args:
        text (str): The input text to split.

    Returns:
        List[str]: A list of sentences extracted from the input text.
    """
    sentences: List[str] = re.split(r'(?<=[.!?])[\s\n]+', text.strip())
    return sentences

def encode(sentence: str, model: SentenceTransformer) -> sentence_embedding.SentenceEmbedding:
    """
    Encodes a given sentence into its embedding representation.

    Args:
        sentence (str): The input sentence to encode.
        model (SentenceTransformer): The SentenceTransformer model to use for encoding.

    Returns:
        sentence_embedding.SentenceEmbedding: An object representing the sentence embedding.
    """
    embedding: Any = model.encode(sentence, convert_to_tensor=True)
    embedding_numpy: np.ndarray = embedding.cpu().detach().numpy()
    
    # Create an instance of the SentenceEmbedding class defined in C++
    sentence_embedding_obj: sentence_embedding.SentenceEmbedding = sentence_embedding.SentenceEmbedding(sentence, embedding_numpy)
    
    return sentence_embedding_obj

@app.route('/')
def index() -> str:
    """
    Renders the index HTML page.

    Returns:
        str: The rendered HTML page.
    """
    return render_template('index.html')

@app.route('/answers', methods=['POST'])
def get_answers() -> Dict[str, Any]:
    """
    Returns the most similar sentence from the essay for each query.
    
    Expected JSON input:
    {
        "essay": str,
        "queries": List[str]
    }

    Returns:
    {
        "answers": List[str]
    }
    """
    data: Dict[str, Any] = request.get_json()
    essay: str = data.get('essay', "")
    queries: List[str] = data.get('queries', [])

    if not essay or not queries:
        return jsonify({"error": "Essay and queries are required."}), 400

    sentences_list: List[sentence_embedding.SentenceEmbedding] = []
    for sentence in text_to_sentence(essay):
        sentence_embedding_obj: sentence_embedding.SentenceEmbedding = encode(sentence, model)
        sentences_list.append(sentence_embedding_obj)

    answers: List[str] = []
    for query in queries:
        query_obj: sentence_embedding.SentenceEmbedding = encode(query, model)
        most_similar: tuple[int, float] = query_obj.get_most_similar(sentences_list, "cosine")
        answer: str = sentences_list[most_similar[0]].get_sentence() if most_similar[0] != -1 else "No similar sentence found."
        answers.append(answer)

    return jsonify({"answers": answers})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
