import os
import time
import logging
import socket
from typing import Optional

# AI Investor Imports
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def run_speed_test(service: str):
    """
    Entry point for speedtest remote <service>
    """
    service = service.lower()
    
    if service == "postgres":
        test_postgres_speed()
    elif service == "redis":
        test_redis_speed()
    elif service == "neo4j":
        test_neo4j_speed()
    elif service == "kafka":
        test_kafka_speed()
    else:
        print(f"Error: Unsupported service '{service}'")

def test_postgres_speed():
    import psycopg2
    db_url = os.getenv("DATABASE_URL")
    print(f"Testing Postgres latency on {os.getenv('POSTGRES_HOST')}...")
    
    try:
        start_time = time.perf_counter()
        conn = psycopg2.connect(db_url, connect_timeout=3)
        connect_time = (time.perf_counter() - start_time) * 1000
        
        cursor = conn.cursor()
        start_query = time.perf_counter()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        query_time = (time.perf_counter() - start_query) * 1000
        
        conn.close()
        print(f"[OK] Postgres Speed:")
        print(f"     - Connection: {connect_time:.2f} ms")
        print(f"     - Query (SELECT 1): {query_time:.2f} ms")
        print(f"     - Total: {(connect_time + query_time):.2f} ms")
    except Exception as e:
        print(f"[ERROR] Postgres speed test failed: {e}")

def test_redis_speed():
    import redis
    host = os.getenv("REDIS_HOST") or "127.0.0.1"
    password = os.getenv("REDIS_PASSWORD")
    print(f"Testing Redis latency on {host}...")
    
    try:
        r = redis.Redis(host=host, port=6379, password=password, socket_timeout=3)
        
        latencies = []
        for _ in range(5):
            start = time.perf_counter()
            r.ping()
            latencies.append((time.perf_counter() - start) * 1000)
        
        avg_latency = sum(latencies) / len(latencies)
        print(f"[OK] Redis Speed (Avg of 5 PINGs): {avg_latency:.2f} ms")
    except Exception as e:
        print(f"[ERROR] Redis speed test failed: {e}")

def test_neo4j_speed():
    from neo4j import GraphDatabase
    uris = [
        os.getenv("NEO4J_URI"),
        f"bolt://{os.getenv('NEO4J_HOST')}:7687",
        f"neo4j://{os.getenv('NEO4J_HOST')}:7687"
    ]
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    success = False
    for uri in uris:
        if not uri: continue
        print(f"Testing Neo4j latency on {uri}...")
        try:
            start_time = time.perf_counter()
            driver = GraphDatabase.driver(uri, auth=(user, password))
            driver.verify_connectivity()
            connect_time = (time.perf_counter() - start_time) * 1000
            
            with driver.session() as session:
                start_query = time.perf_counter()
                session.run("RETURN 1").single()
                query_time = (time.perf_counter() - start_query) * 1000
                
            driver.close()
            print(f"[OK] Neo4j Speed (via {uri}):")
            print(f"     - Connection/Auth: {connect_time:.2f} ms")
            print(f"     - Query (RETURN 1): {query_time:.2f} ms")
            print(f"     - Total: {(connect_time + query_time):.2f} ms")
            success = True
            break
        except Exception as e:
            print(f"     - {uri} failed: {e}")
    
    if not success:
        print(f"[FAIL] Neo4j: All connection attempts failed.")

def test_kafka_speed():
    from kafka import KafkaProducer, KafkaConsumer
    import uuid
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    topic = f"speedtest-{uuid.uuid4()}"
    print(f"Testing Kafka round-trip latency on {bootstrap_servers}...")
    
    try:
        # Producer
        start_prod = time.perf_counter()
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers, 
            request_timeout_ms=2000,
            api_version_auto_timeout_ms=2000
        )
        prod_init_time = (time.perf_counter() - start_prod) * 1000
        
        # Consumer
        start_cons = time.perf_counter()
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            consumer_timeout_ms=2000,
            request_timeout_ms=2000
        )
        cons_init_time = (time.perf_counter() - start_cons) * 1000
        
        # Round-trip
        start_rt = time.perf_counter()
        producer.send(topic, b"speed-test-data")
        producer.flush()
        
        message_received = False
        for message in consumer:
            if message.value == b"speed-test-data":
                message_received = True
                break
        
        rt_time = (time.perf_counter() - start_rt) * 1000
        
        producer.close()
        consumer.close()
        
        if message_received:
            print(f"[OK] Kafka Speed:")
            print(f"     - Producer Init: {prod_init_time:.2f} ms")
            print(f"     - Consumer Init: {cons_init_time:.2f} ms")
            print(f"     - Round-trip (Send/Poll): {rt_time:.2f} ms")
        else:
            print(f"[FAIL] Kafka: Message sent but not received within timeout.")
            
    except Exception as e:
        print(f"[ERROR] Kafka speed test failed: {e}")
