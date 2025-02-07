import os
from dotenv import load_dotenv
import openai
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Charger les variables d'environnement
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("La clé API OpenAI est manquante. Ajoutez-la dans le fichier .env")

# Initialisation du client OpenAI
openai_client = openai.Client(api_key=OPENAI_API_KEY)

# Définition du chemin de la base ChromaDB
CHROMA_DB_DIR = "../vector_database/chroma_db"


# Initialisation de ChromaDB
def get_chroma_collection():
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings, collection_name="history_france")


# Initialisation de la base vectorielle
vectorstore = get_chroma_collection()


def generate_rag_response(messages, query, top_k=3):
    print("\n🔍 Recherche des documents pertinents...")
    results = vectorstore.similarity_search(query, k=top_k)

    if not results:
        return "Je n'ai pas trouvé d'informations pertinentes pour répondre à ta question."

    # Construire le contexte avec les chunks récupérés et inclure les sources
    context = "\n\n".join([
                              f"Source: {doc.metadata.get('title', 'Inconnue')} - {doc.metadata.get('url', 'URL non disponible')}\n{doc.page_content}"
                              for doc in results])

    # Construire le prompt pour GPT-4
    prompt = f"""
    Tu es un expert en histoire. Réponds à la question suivante en utilisant le contexte fourni et tes connaissances.

    ### CONTEXTE :
    {context}

    ### QUESTION :
    {query}

    À la fin de ta réponse, affiche les sources sous ce format :

    ---
    **Sources :**
    - [Nom de la source](lien)
    - [Autre source](lien)
    ---

    """

    print("\n📝 Envoi de la requête à GPT-4...")

    messages = [*messages, {"role": "user", "content": prompt}]
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content
