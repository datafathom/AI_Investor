"""
==============================================================================
AI Investor - Neo4j Schema Initialization
==============================================================================
PURPOSE:
    Initialize the Neo4j graph database schema for the AI Investor system.
    Creates nodes for assets, sectors, and indices plus relationships
    for tracking correlations, holdings, and liquidity paths.

USAGE:
    python scripts/neo4j/init_schema.py --create
    
SCHEMA DESIGN:
    Nodes:
        - Asset: Individual stocks and ETFs with properties
        - Sector: Market sectors (Technology, Energy, etc.)
        - Index: Market indices (SPY, QQQ, VIX)
        - Strategy: Trading strategies
        
    Relationships:
        - BELONGS_TO: Asset -> Sector
        - TRACKS: ETF -> Index
        - CORRELATES_WITH: Asset <-> Asset (with correlation coefficient)
        - HOLDS: ETF -> Asset (with weight)
==============================================================================
"""
from typing import Any, Dict, List, Optional
import os
import logging

logger = logging.getLogger(__name__)


# Schema definitions
NODE_LABELS = {
    'Asset': {
        'description': 'Individual tradeable securities (stocks, ETFs)',
        'properties': ['symbol', 'name', 'asset_type', 'market_cap', 'avg_volume'],
        'indices': ['symbol']
    },
    'Sector': {
        'description': 'Market sectors for classification',
        'properties': ['name', 'gics_code'],
        'indices': ['name']
    },
    'Index': {
        'description': 'Market indices and benchmarks',
        'properties': ['symbol', 'name', 'index_type'],
        'indices': ['symbol']
    },
    'Strategy': {
        'description': 'Trading strategies and signals',
        'properties': ['name', 'strategy_type', 'risk_level', 'is_active'],
        'indices': ['name']
    }
}

RELATIONSHIP_TYPES = {
    'BELONGS_TO': {
        'description': 'Asset belongs to Sector',
        'from_label': 'Asset',
        'to_label': 'Sector'
    },
    'TRACKS': {
        'description': 'ETF tracks an Index',
        'from_label': 'Asset',
        'to_label': 'Index',
        'properties': ['tracking_error']
    },
    'CORRELATES_WITH': {
        'description': 'Correlation between assets',
        'from_label': 'Asset',
        'to_label': 'Asset',
        'properties': ['correlation', 'lookback_days', 'updated_at']
    },
    'HOLDS': {
        'description': 'ETF holds constituent assets',
        'from_label': 'Asset',
        'to_label': 'Asset',
        'properties': ['weight', 'shares']
    },
    'SIGNALS': {
        'description': 'Strategy generates signal for Asset',
        'from_label': 'Strategy',
        'to_label': 'Asset',
        'properties': ['signal_strength', 'generated_at']
    }
}

# Sample data for initial population
SAMPLE_SECTORS = [
    {'name': 'Technology', 'gics_code': '45'},
    {'name': 'Healthcare', 'gics_code': '35'},
    {'name': 'Financials', 'gics_code': '40'},
    {'name': 'Energy', 'gics_code': '10'},
    {'name': 'Consumer Discretionary', 'gics_code': '25'},
    {'name': 'Industrials', 'gics_code': '20'},
    {'name': 'Materials', 'gics_code': '15'},
    {'name': 'Utilities', 'gics_code': '55'},
    {'name': 'Real Estate', 'gics_code': '60'},
    {'name': 'Communication Services', 'gics_code': '50'},
    {'name': 'Consumer Staples', 'gics_code': '30'},
]

SAMPLE_INDICES = [
    {'symbol': 'SPX', 'name': 'S&P 500', 'index_type': 'broad_market'},
    {'symbol': 'NDX', 'name': 'NASDAQ 100', 'index_type': 'broad_market'},
    {'symbol': 'VIX', 'name': 'CBOE Volatility Index', 'index_type': 'volatility'},
    {'symbol': 'DJI', 'name': 'Dow Jones Industrial', 'index_type': 'blue_chip'},
    {'symbol': 'RUT', 'name': 'Russell 2000', 'index_type': 'small_cap'},
]

SAMPLE_ASSETS = [
    {'symbol': 'SPY', 'name': 'SPDR S&P 500 ETF', 'asset_type': 'ETF', 'sector': 'Broad Market'},
    {'symbol': 'QQQ', 'name': 'Invesco QQQ Trust', 'asset_type': 'ETF', 'sector': 'Technology'},
    {'symbol': 'UVXY', 'name': 'ProShares Ultra VIX', 'asset_type': 'ETF', 'sector': 'Volatility'},
    {'symbol': 'SVXY', 'name': 'ProShares Short VIX', 'asset_type': 'ETF', 'sector': 'Volatility'},
    {'symbol': 'XLK', 'name': 'Technology Select Sector', 'asset_type': 'ETF', 'sector': 'Technology'},
    {'symbol': 'XLF', 'name': 'Financial Select Sector', 'asset_type': 'ETF', 'sector': 'Financials'},
    {'symbol': 'XLE', 'name': 'Energy Select Sector', 'asset_type': 'ETF', 'sector': 'Energy'},
    {'symbol': 'IWM', 'name': 'iShares Russell 2000', 'asset_type': 'ETF', 'sector': 'Broad Market'},
    {'symbol': 'TLT', 'name': 'iShares 20+ Year Treasury', 'asset_type': 'ETF', 'sector': 'Fixed Income'},
    {'symbol': 'GLD', 'name': 'SPDR Gold Shares', 'asset_type': 'ETF', 'sector': 'Commodities'},
]


class Neo4jSchemaManager:
    """
    Manager for Neo4j schema creation and initialization.
    
    Handles constraint creation, index management, and initial data population.
    
    Attributes:
        uri (str): Neo4j connection URI.
        auth (tuple): Authentication credentials.
        driver: Neo4j driver instance (lazy loaded).
    """
    
    def __init__(
        self,
        uri: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> None:
        """
        Initialize the Neo4j Schema Manager.
        
        Args:
            uri: Neo4j connection URI. Defaults to env var.
            username: Database username. Defaults to env var.
            password: Database password. Defaults to env var.
        """
        self.uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.auth = (
            username or os.getenv('NEO4J_USER', 'neo4j'),
            password or os.getenv('NEO4J_PASSWORD', 'investor_password')
        )
        self._driver = None
        logger.info(f"Neo4jSchemaManager initialized for {self.uri}")
    
    @property
    def driver(self):
        """Lazy-load the Neo4j driver."""
        if self._driver is None:
            try:
                from neo4j import GraphDatabase
                self._driver = GraphDatabase.driver(self.uri, auth=self.auth)
            except ImportError:
                logger.error("neo4j driver not installed. Run: pip install neo4j")
                raise
        return self._driver
    
    def close(self) -> None:
        """Close the database connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def _run_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Run a Cypher query and return results."""
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
    
    def create_constraints(self) -> Dict[str, bool]:
        """
        Create uniqueness constraints for node labels.
        
        Returns:
            Dictionary mapping constraint names to success status.
        """
        results = {}
        
        for label, config in NODE_LABELS.items():
            for prop in config.get('indices', []):
                constraint_name = f"unique_{label.lower()}_{prop}"
                try:
                    query = f"""
                    CREATE CONSTRAINT {constraint_name} IF NOT EXISTS
                    FOR (n:{label})
                    REQUIRE n.{prop} IS UNIQUE
                    """
                    self._run_query(query)
                    results[constraint_name] = True
                    logger.info(f"✅ Created constraint: {constraint_name}")
                except Exception as e:
                    logger.error(f"❌ Failed to create constraint {constraint_name}: {e}")
                    results[constraint_name] = False
        
        return results
    
    def create_indices(self) -> Dict[str, bool]:
        """
        Create additional indices for performance.
        
        Returns:
            Dictionary mapping index names to success status.
        """
        additional_indices = [
            ('idx_asset_type', 'Asset', 'asset_type'),
            ('idx_strategy_active', 'Strategy', 'is_active'),
        ]
        
        results = {}
        for idx_name, label, prop in additional_indices:
            try:
                query = f"""
                CREATE INDEX {idx_name} IF NOT EXISTS
                FOR (n:{label})
                ON (n.{prop})
                """
                self._run_query(query)
                results[idx_name] = True
                logger.info(f"✅ Created index: {idx_name}")
            except Exception as e:
                logger.error(f"❌ Failed to create index {idx_name}: {e}")
                results[idx_name] = False
        
        return results
    
    def populate_sectors(self) -> int:
        """
        Populate Sector nodes with sample data.
        
        Returns:
            Number of sectors created.
        """
        count = 0
        for sector in SAMPLE_SECTORS:
            try:
                query = """
                MERGE (s:Sector {name: $name})
                SET s.gics_code = $gics_code
                RETURN s
                """
                self._run_query(query, sector)
                count += 1
            except Exception as e:
                logger.error(f"Failed to create sector {sector['name']}: {e}")
        
        logger.info(f"Created {count} Sector nodes")
        return count
    
    def populate_indices(self) -> int:
        """
        Populate Index nodes with sample data.
        
        Returns:
            Number of indices created.
        """
        count = 0
        for index in SAMPLE_INDICES:
            try:
                query = """
                MERGE (i:Index {symbol: $symbol})
                SET i.name = $name, i.index_type = $index_type
                RETURN i
                """
                self._run_query(query, index)
                count += 1
            except Exception as e:
                logger.error(f"Failed to create index {index['symbol']}: {e}")
        
        logger.info(f"Created {count} Index nodes")
        return count
    
    def populate_assets(self) -> int:
        """
        Populate Asset nodes with sample data.
        
        Returns:
            Number of assets created.
        """
        count = 0
        for asset in SAMPLE_ASSETS:
            try:
                query = """
                MERGE (a:Asset {symbol: $symbol})
                SET a.name = $name, a.asset_type = $asset_type
                RETURN a
                """
                self._run_query(query, asset)
                count += 1
            except Exception as e:
                logger.error(f"Failed to create asset {asset['symbol']}: {e}")
        
        logger.info(f"Created {count} Asset nodes")
        return count
    
    def create_relationships(self) -> int:
        """
        Create sample relationships between nodes.
        
        Returns:
            Number of relationships created.
        """
        relationships = [
            # ETF -> Index tracking
            ("SPY", "TRACKS", "SPX"),
            ("QQQ", "TRACKS", "NDX"),
            ("IWM", "TRACKS", "RUT"),
            # Sector ETF -> Sector
            ("XLK", "BELONGS_TO", "Technology"),
            ("XLF", "BELONGS_TO", "Financials"),
            ("XLE", "BELONGS_TO", "Energy"),
        ]
        
        count = 0
        for from_sym, rel_type, to_sym in relationships:
            try:
                if rel_type == "TRACKS":
                    query = """
                    MATCH (a:Asset {symbol: $from_sym})
                    MATCH (i:Index {symbol: $to_sym})
                    MERGE (a)-[:TRACKS]->(i)
                    """
                elif rel_type == "BELONGS_TO":
                    query = """
                    MATCH (a:Asset {symbol: $from_sym})
                    MATCH (s:Sector {name: $to_sym})
                    MERGE (a)-[:BELONGS_TO]->(s)
                    """
                else:
                    continue
                
                self._run_query(query, {'from_sym': from_sym, 'to_sym': to_sym})
                count += 1
            except Exception as e:
                logger.error(f"Failed to create relationship {from_sym}->{to_sym}: {e}")
        
        logger.info(f"Created {count} relationships")
        return count
    
    def initialize_schema(self) -> Dict[str, Any]:
        """
        Full schema initialization: constraints, indices, and sample data.
        
        Returns:
            Summary of initialization results.
        """
        logger.info("Starting Neo4j schema initialization...")
        
        results = {
            'constraints': self.create_constraints(),
            'indices': self.create_indices(),
            'sectors_created': self.populate_sectors(),
            'indices_created': self.populate_indices(),
            'assets_created': self.populate_assets(),
            'relationships_created': self.create_relationships(),
        }
        
        logger.info("Schema initialization complete")
        return results
    
    def get_node_counts(self) -> Dict[str, int]:
        """
        Get count of nodes by label.
        
        Returns:
            Dictionary mapping labels to node counts.
        """
        counts = {}
        for label in NODE_LABELS.keys():
            result = self._run_query(f"MATCH (n:{label}) RETURN count(n) as count")
            counts[label] = result[0]['count'] if result else 0
        return counts
    
    def verify_schema(self) -> Dict[str, Any]:
        """
        Verify schema is properly initialized.
        
        Returns:
            Verification results with node counts and relationship stats.
        """
        node_counts = self.get_node_counts()
        
        rel_result = self._run_query("""
            MATCH ()-[r]->()
            RETURN type(r) as type, count(r) as count
        """)
        rel_counts = {r['type']: r['count'] for r in rel_result}
        
        return {
            'node_counts': node_counts,
            'relationship_counts': rel_counts,
            'total_nodes': sum(node_counts.values()),
            'total_relationships': sum(rel_counts.values())
        }


def main():
    """CLI entry point for schema initialization."""
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='Neo4j Schema Manager')
    parser.add_argument('--uri', default=None, help='Neo4j URI')
    parser.add_argument('--create', action='store_true', help='Create schema and populate data')
    parser.add_argument('--verify', action='store_true', help='Verify schema exists')
    parser.add_argument('--counts', action='store_true', help='Show node counts')
    
    args = parser.parse_args()
    
    manager = Neo4jSchemaManager(uri=args.uri)
    
    try:
        if args.create:
            results = manager.initialize_schema()
            print("\nSchema initialization results:")
            print(f"  Sectors: {results['sectors_created']}")
            print(f"  Indices: {results['indices_created']}")
            print(f"  Assets: {results['assets_created']}")
            print(f"  Relationships: {results['relationships_created']}")
        
        elif args.verify:
            results = manager.verify_schema()
            print("\nSchema verification:")
            print(f"  Total nodes: {results['total_nodes']}")
            print(f"  Total relationships: {results['total_relationships']}")
            for label, count in results['node_counts'].items():
                print(f"    {label}: {count}")
        
        elif args.counts:
            counts = manager.get_node_counts()
            print("\nNode counts:")
            for label, count in counts.items():
                print(f"  {label}: {count}")
        
        else:
            parser.print_help()
    
    finally:
        manager.close()


if __name__ == '__main__':
    main()
