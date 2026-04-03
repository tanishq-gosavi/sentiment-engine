import json
import time
import requests
from kafka import KafkaProducer

# Initialize Kafka Producer
# Assumes Kafka is running locally on default port 9092
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

FINNHUB_API_KEY = "d77lrt1r01qp6afm2sh0d77lrt1r01qp6afm2shg"
KAFKA_TOPIC = 'financial-news'

def fetch_and_publish_news():
    url = "https://finnhub.io/api/v1/news?category=general&token=d77lrt1r01qp6afm2sh0d77lrt1r01qp6afm2shg"
    
    while True:
        try:
            response = requests.get(url)
            news_items = response.json()
            
            # Grab the top 5 latest headlines
            for item in news_items[:5]:
                payload = {
                    "id": item['id'],
                    "headline": item['headline'],
                    "summary": item['summary'],
                    "url": item['url'],
                    "timestamp": item['datetime']
                }
                
                # Send to Kafka
                producer.send(KAFKA_TOPIC, payload)
                print(f"Published: {item['headline']}")
                
            # Wait 60 seconds before fetching again
            time.sleep(60)
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            time.sleep(10)

if __name__ == "__main__":
    print("Starting Financial News Producer...")
    fetch_and_publish_news()