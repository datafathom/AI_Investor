import unittest
from services.neo4j.node_factory import NodeFactory
from services.neo4j.relationship_builder import RelationshipBuilder
from services.kafka.graph_consumer import GraphConsumerService

class TestNeo4jRebuild(unittest.TestCase):

    def setUp(self):
        self.node_factory = NodeFactory()
        self.rel_builder = RelationshipBuilder()
        self.consumer = GraphConsumerService()

    def test_create_asset_node(self):
        """Test asset node creation properties."""
        props = self.node_factory.create_asset_node("AAPL", "EQUITY")
        self.assertEqual(props["label"], "ASSET")
        self.assertEqual(props["symbol"], "AAPL")
        self.assertTrue("id" in props)

    def test_create_agent_node(self):
        """Test agent node creation properties."""
        props = self.node_factory.create_agent_node("RiskBot", "WATCHER")
        self.assertEqual(props["label"], "AGENT")
        self.assertEqual(props["persona"], "WATCHER")

    def test_build_relationship(self):
        """Test relationship construction."""
        rel = self.rel_builder.build_ownership_rel("entity-123", "asset-456", 100.0)
        self.assertEqual(rel["type"], "OWNS")
        self.assertEqual(rel["properties"]["quantity"], 100.0)

    def test_consumer_init(self):
        """Test consumer initialization."""
        self.assertIsNotNone(self.consumer)
        # Just verifying it doesn't crash on init
        self.consumer.process_event({"type": "TEST_EVENT"})

if __name__ == '__main__':
    unittest.main()
