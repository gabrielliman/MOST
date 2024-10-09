import re
import numpy as np
import sentence_embedding  # Import C++ class
from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)   

# Initialize the SentenceTransformer model outside of the route
model = SentenceTransformer("all-mpnet-base-v2")

def text_to_sentence(text: str) -> list[str]:
    # Usa expressão regular para dividir o texto nas pontuações que indicam fim de frase
    sentences = re.split(r'(?<=[.!?])[\s\n]+', text.strip())
    return sentences

def encode(sentence: str, model: SentenceTransformer) -> sentence_embedding.SentenceEmbedding:
    # Codificar a sentença
    embedding = model.encode(sentence, convert_to_tensor=True)

    # Converter o tensor do Torch para um array NumPy
    embedding_numpy = embedding.cpu().detach().numpy()

    # Criar uma instância da classe SentenceEmbedding definida em C++
    sentence_embedding_obj = sentence_embedding.SentenceEmbedding(sentence, embedding_numpy)
    
    return sentence_embedding_obj

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/answers', methods=['POST'])
def get_answers():
    data = request.get_json()
    essay = data.get('essay')
    queries = data.get('queries', [])

    if not essay or not queries:
        return jsonify({"error": "Essay and queries are required."}), 400

    sentences_list = []
    for sentence in text_to_sentence(essay):
        sentence_embedding_obj = encode(sentence, model)
        sentences_list.append(sentence_embedding_obj)

    answers = []
    for query in queries:
        query_obj=encode(query,model)
        most_similar = query_obj.get_most_similar(sentences_list, "cosine")
        answer = sentences_list[most_similar[0]].get_sentence() if most_similar[0] != -1 else "No similar sentence found."
        answers.append(answer)

    return jsonify({"answers": answers})

if __name__ == "__main__":
    app.run(debug=True) 