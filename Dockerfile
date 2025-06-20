FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY .env .
COPY . .

# Streamlit-specific config to avoid "can't open browser" issues in containers
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false

# Expose the Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app/app.py"]