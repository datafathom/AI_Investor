"""
==============================================================================
FILE: web/routes/system_routes.py
ROLE: System Monitoring API Blueprint
PURPOSE: Exposes endpoints for system health and infrastructure monitoring:
         - Kafka Cluster Status
         - Kafka Throughput Stats
         - Service Health Checks
         
ARCHITECTURE:
    - Flask Blueprint.
    - Interfaces with KafkaMonitorService (AdminClient).
    
DEPENDENCIES:
    - flask
    - services.system.kafka_monitor_service
==============================================================================
"""

from flask import Blueprint, jsonify
from services.system.kafka_monitor_service import kafka_monitor_service

# Define Blueprint
system_bp = Blueprint('system_bp', __name__, url_prefix='/api/v1/system')

@system_bp.route('/kafka/status', methods=['GET'])
async def get_kafka_status():
    """
    Get Kafka cluster health, topic count, and broker info.
    """
    data = await kafka_monitor_service.get_cluster_status()
    return jsonify(data)

@system_bp.route('/kafka/stats', methods=['GET'])
async def get_kafka_stats():
    """
    Get simulated throughput statistics for Kafka topics.
    Real implementation would query JMX/Prometheus.
    """
    data = await kafka_monitor_service.get_throughput_stats()
    return jsonify(data)
