# 🧠 AI Data Analyst – Proof of Concept

This is a proof-of-concept (PoC) for an AI-powered data analyst. It allows business users to:

- ✅ Upload Excel datasets
- ✅ Ask natural language questions
- ✅ Automatically generate SQL queries
- ✅ Run those queries on structured data
- ✅ Receive AI-generated summaries and insights

---

## 🚀 Features

- 🤖 Uses GPT-4o(-mini) to translate questions into SQL
- 📊 Executes SQL queries on a local SQLite database
- 💡 AI interprets query results to provide insights
- 🖥️ Simple UI built with Streamlit
- 🐳 Dockerized for easy deployment

---

## 🗂️ Project Structure

ai-data-analyst-poc\ <br>
| <br>
|_app\ <br>
|____db\ <br>
|______db.py <br>
|______my_db.db <br>
|____services\ <br>
|______llm_service.py <br>
|______query_executor.py <br>
|____app.py <br/>
|_dockerignore <br>
|_Dockerfile <br>
|_env <br>
|_requirements.txt <br>
|_README.md


---

## ⚙️ Installation & Usage

### ▶️ Run Locally

1. Clone the repo:
    ```bash
    git clone repo
    cd ai-data-analyst-poc
    ```

2. Set up virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set environment variables in `.env`:
    ```env
    API_KEY=your-openai-api-key
    PATH_TO_DB=/absolute/or/relative/path/to/db/my_db.db
    PATH_TO_DATA=/absolute/or/relative/path/to/data/Data_Pump.xlsx
    ```

5. Run the app:
    ```bash
    streamlit run app.py
    ```

---

### 🐳 Run with Docker

1. Build Docker image:
    ```bash
    docker build -t ai-data-analyst .
    ```

2. Run container:
    ```bash
    docker run -p 8501:8501 ai-data-analyst
    ```

3. Open [http://localhost:8501](http://localhost:8501)

---

## 📥 Uploading Data

- Upload `.xlsx` files using the UI.
- The app converts them into a temporary SQLite database.
- You can then ask natural questions like:
  > "Which months had the highest revenue?"  
  > "What is the highest/lowest transaction value for each Posting period?"

---

## 🧠 Technologies Used

- **OpenAI GPT-4o(-mini)** – Natural language to SQL + Insight generation
- **Streamlit** – UI
- **SQLite** – Lightweight local database
- **Python** – Main language
- **Docker** – Deployment & containerization
- **FastAPI (optional)** – For backend services (can be added later)
---

## 📌 TODO / Ideas for Improvement

- Add support for chart suggestions & visualizations
- Improve error handling / SQL retry logic
- Add advanced full-scale backend with FastAPI
- Add user authentication (if used in production)
- Expand LLM prompt training with few-shot examples
