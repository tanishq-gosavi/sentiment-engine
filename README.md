# AI-Powered Financial Sentiment Engine
A real-time data streaming platform that analyzes live financial news using **FinBERT** and **Apache Kafka**.

## Architecture
- **Data Pipeline:** Python script fetching live news from Finnhub API.
- **Message Broker:** Apache Kafka (running in Docker) for high-throughput data streaming.
- **ML Backend:** Flask server running a FinBERT Transformer model for sentiment analysis.
- **Frontend:** React + Vite dashboard with live Recharts visualization.

## Setup
1. Start the infrastructure: `docker compose up -d`
2. Run the Pipeline: `cd data-pipeline && python producer.py`
3. Run the Backend: `cd ml-backend && python app.py`
4. Run the UI: `cd frontend && npm run dev`
=======
# sentiment-engine
>>>>>>> 884cca7317d1877e4b8a5f3aee97849263362506
