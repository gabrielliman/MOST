import re
import numpy as np
import sentence_embedding  # Import C++ class
from sentence_transformers import SentenceTransformer

def input_reading() -> (str, list[str]):
    # Leitura direta do arquivo durante fases iniciais do programa
    f = open("essay.txt", "r")
    essay = f.read()

    queries = []
    with open("queries.txt", 'r') as file:
        for line in file:
            queries.append(line.strip())

    return essay, queries

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

def main():
    essay, queries = input_reading()
    model = SentenceTransformer("all-mpnet-base-v2")

    for sentence in text_to_sentence(essay):
        print(sentence, "\n")
        sentence_embedding_obj = encode(sentence, model)
        print(sentence_embedding_obj.get_sentence())
        print(sentence_embedding_obj.get_embeddings())

if __name__ == "__main__":
    main()
