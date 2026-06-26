import json
import time
from confluent_kafka import Producer, Consumer, KafkaError

KAFKA_BROKER = "localhost:9092"
TARGET_TOPIC = "telemetry.scraping.logs"

# =====================================================================
# 1. THE PRODUCER LAYER (The Ingestion Client)
# =====================================================================
class DataStreamProducer:
    def __init__(self, broker: str):
        config = {'bootstrap.servers': broker}
        self.producer = Producer(config)

    def _delivery_report(self, err, msg):
        """Callback triggered once the Kafka broker safely writes the event to disk."""
        if err is not None:
            print(f"❌ Event delivery failed: {err}")
        else:
            print(f"🛰️ Event buffered in partition [{msg.partition()}] at offset {msg.offset()}")

    def publish_event(self, topic: str, key: str, payload: dict):
        """Fires an isolated telemetry event into the distributed broker log."""
        serialized_data = json.dumps(payload).encode('utf-8')
        
        # Non-blocking asynchronous message delivery
        self.producer.produce(
            topic, 
            key=key, 
            value=serialized_data, 
            callback=self._delivery_report
        )
        # Polls the local event queue to trigger callback alerts
        self.producer.poll(0) 

    def flush_buffers(self):
        self.producer.flush()

# =====================================================================
# 2. THE CONSUMER LAYER (The Background Processing Core)
# =====================================================================
def run_stream_consumer(broker: str, topic: str):
    """Runs a continuous listener loop that processes incoming events from the log."""
    config = {
        'bootstrap.servers': broker,
        'group.id': 'analytics-consumer-group', # Identifies this cluster scale instance
        'auto.offset.reset': 'earliest',         # Read from the start of the log if new
        'enable.auto.commit': True
    }
    
    consumer = Consumer(config)
    consumer.subscribe([topic])
    
    print(f"📥 Consumer stream initialized. Listening for messages on topic [{topic}]...")
    
    try:
        # Continuous non-blocking message loop
        for _ in range(3): 
            msg = consumer.poll(timeout=1.0) # Wait for a message up to 1 second
            
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"⚠️ Consumer Error encountered: {msg.error()}")
                    break
                    
            # Extract and deserialize byte vectors back into native dictionary items
            event_key = msg.key().decode('utf-8') if msg.key() else "Unknown"
            event_data = json.loads(msg.value().decode('utf-8'))
            
            print(f"⚡ [Stream Processing] Key: {event_key} | Processed Payload: {event_data}")
            
    finally:
        consumer.close()

# =====================================================================
# 3. CONCURRENCY SIMULATION RUNNER
# =====================================================================
def simulate_streaming_ecosystem():
    # Inside a real production network, these components live on entirely different servers
    print("🎬 Simulating live Distributed Event Stream...")
    
    # Initialize and fire messages from our Producer client
    # (Wrapped in a try block to handle broker-not-found exceptions gracefully during testing)
    try:
        stream_client = DataStreamProducer(broker=KAFKA_BROKER)
        
        mock_log = {"node": "Scraper_Node_4", "char_count": 4500, "status": "Success"}
        stream_client.publish_event(topic=TARGET_TOPIC, key="Node_4", payload=mock_log)
        
        # Ensure all internal network buffers are cleared
        stream_client.flush_buffers()
    except Exception as e:
        print(f"⚠️ Simulation note: Broker connection bypassed. ({e})")
        print("💡 In real production deployment, this writes directly to your scalable cluster.")

if __name__ == "__main__":
    simulate_streaming_ecosystem()
