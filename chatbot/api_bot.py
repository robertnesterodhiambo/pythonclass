import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings  # Local embeddings
from langchain_community.vectorstores import Chroma
from llama_cpp import Llama

# 1. Load PDFs from Folder
def load_pdfs_from_folder(folder_path):
    all_docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            all_docs.extend(pages)
    return all_docs

# 2. Convert Text to Embeddings and Store in a Vector DB
def create_vector_db(documents):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # Local model
    vector_db = Chroma.from_documents(documents, embedding_model)
    return vector_db

# 3. Load LLaMA Model
def load_llama(model_path):
    return Llama(model_path=model_path)

# 4. Answer Questions Based on PDF Content (Limits context length)
def answer_question(vector_db, llm, question, max_context_tokens=300):
    similar_docs = vector_db.similarity_search(question, k=3)  # Retrieve top 3 relevant pages
    
    # Combine retrieved documents and truncate to avoid exceeding LLaMA's context window
    context = "\n".join([doc.page_content for doc in similar_docs])
    context = " ".join(context.split()[:max_context_tokens])  # Truncate to max 300 tokens

    prompt = f"Answer the question based on the context and you are a very helpful AI chat assistant customer care:\n\n{context}\n\nQ: {question}\nA:"

    # Reduce max_tokens to ensure it fits within the model's 512-token context window
    response = llm(prompt, max_tokens=100, stop=["Q:", "\n\n"])  # Adding stop sequences
    return response['choices'][0]['text']


# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    pdf_folder = "/home/dragon/Bob/pythonclass/chatbot/pdfs"  # Change this to your actual folder path
    model_path = "/home/dragon/Downloads/llama-2-7b.Q2_K.gguf"  # Change this to your LLaMA model path
    
    print("Loading PDFs...")
    documents = load_pdfs_from_folder(pdf_folder)
    print(f"Loaded {len(documents)} pages from PDFs.")
    
    print("Creating Vector Database...")
    vector_db = create_vector_db(documents)
    
    print("Loading LLaMA Model...")
    llm = load_llama(model_path)
    
    while True:
        question = input("Ask a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        answer = answer_question(vector_db, llm, question)
        print(f"Answer: {answer}\n")
