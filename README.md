# LangGraph-RAG-Router
A workflow that leverages LangGraph for query routing and RAG for context-aware responses from vector databases.

## ✨ Features

**1.** **Query Categorization:** Automatically classifies queries as `weather`, `jobsite_related`, or `general`.

**2.** **Conditional Routing:** Directs queries to the appropriate tool based on category.

**3**. **Jobsite RAG:** Uses a Chroma vector database to retrieve relevant context from PDF documents for jobsite-related queries.

**4.** **Graph-Based Workflow:** Implements a modular, visualizable state graph for query processing.

**5.** **OpenAI Integration:** Uses GPT-4o for prompt-based responses.

**6.** **Easy Extensibility:** Add new categories, tools, or document sources with minimal code changes.


  <p align="center">
  <img width="420" height="333" alt="LangGraphWithRAG" src="https://github.com/user-attachments/assets/5ff424fb-282c-47f6-8705-9f746722659e" />
</p>


## 🚀 Project Structure

- **langGraph_with_RAG.py:** Main workflow and query routing logic.
- **create_db.py:** Script to load, split, embed, and store documents in the Chroma vector database.
- **chroma/**: Directory for vector database files.
- **data/pdf/**: Directory for source PDF documents.
- **LangGraphWithRAG.png:** Mermaid diagram of the workflow graph.
- **.env:** Stores your OpenAI API key.

## ⚙️ Setup & Installation

1. **Clone the repository**
    ```sh
    git clone
    cd LangGraph-RAG-Router
    ```
2. **Create the virtual environment:**
   ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Add your OpenAI API key** to `.env`:
    ```
    OPENAI_API_KEY=your-openai-key
    ```

6. **Prepare your documents:**
    - Place PDFs in `data/pdf/`.

7. **Create the vector database:**
    ```sh
    python3 create_db.py
    ```

8. **Run the main workflow:**
    ```sh
    python3 langGraph_with_RAG.py 
    ```

## ▶️ Usage

- The system will categorize your query and route it to the appropriate tool.
- For jobsite-related queries, it retrieves context from your PDF documents using semantic search.
- The workflow graph is visualized in `LangGraphWithRAG.png`.

## 📜 License
This project is open-source and available under the MIT License.

## 🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

You can also contact me at alishbaahsan127@gmail.com

