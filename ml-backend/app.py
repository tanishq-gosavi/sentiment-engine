import json
import threading
from flask import Flask, jsonify
from flask_cors import CORS
from kafka import KafkaConsumer
from transformers import pipeline

app = Flask(__name__)
CORS(app) # Allows your React frontend to communicate with this API

# Load the pre-trained FinBERT model for financial sentiment analysis
print("Loading ML Model (This may take a moment on first run)...")
sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert", framework="tf")

# Global list to store the latest processed news in memory
processed_news = []

def consume_kafka_messages():
    """Background thread to constantly listen to Kafka and run ML inference"""
    consumer = KafkaConsumer(
        'financial-news',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for message in consumer:
        news_data = message.value
        headline = news_data['headline']
        
        # Run the TensorFlow/FinBERT model
        result = sentiment_pipeline(headline)[0]
        
        # Append sentiment results to our data
        news_data['sentiment'] = result['label'] # positive, negative, or neutral
        news_data['confidence'] = round(result['score'], 4)
        
        # Keep only the latest 50 articles in memory
        global processed_news
        processed_news.insert(0, news_data)
        if len(processed_news) > 50:
            processed_news.pop()
            
        print(f"Analyzed: {headline} -> {result['label']}")

# Start the Kafka consumer in a separate background thread
threading.Thread(target=consume_kafka_messages, daemon=True).start()

@app.route('/api/sentiment/live', methods=['GET'])
def get_live_sentiment():
    """REST endpoint for the React frontend to fetch data"""
    if not processed_news:
        return jsonify({"status": "waiting for data", "data": []}), 200
        
    # Calculate a quick rolling score (e.g., percentage of positive news)
    positives = sum(1 for item in processed_news if item['sentiment'] == 'positive')
    rolling_score = (positives / len(processed_news)) * 100
    
    return jsonify({
        "rolling_bullish_score": round(rolling_score, 2),
        "latest_news": processed_news[:10] # Send the 10 most recent to the UI
    }), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)