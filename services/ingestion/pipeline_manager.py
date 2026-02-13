import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class PipelineRun(BaseModel):
    run_id: str
    pipeline_id: str
    status: str  # "running", "success", "failed"
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = 0.0
    logs: List[str] = []

class PipelineConfig(BaseModel):
    id: str
    name: str
    description: str
    schedule: str  # e.g., "0 9 * * *" or "interval:5m"
    enabled: bool = True
    params: Dict = {}
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: str = "idle"  # "idle", "running", "error"

class PipelineManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PipelineManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.pipelines: Dict[str, PipelineConfig] = {}
        self.runs: Dict[str, List[PipelineRun]] = {}
        self._load_default_pipelines()
        self._initialized = True
        logger.info("PipelineManager initialized.")

    def _load_default_pipelines(self):
        # Seed with initial pipelines as per Phase 5 requirements
        defaults = [
            PipelineConfig(
                id="market_data_sync",
                name="Market Data Sync",
                description="Syncs daily OHLCV data from Alpha Vantage/Polygon.",
                schedule="0 17 * * 1-5"
            ),
            PipelineConfig(
                id="sec_filings_ingest",
                name="SEC 13F Ingestion",
                description="Scrapes and parses new 13F filings from EDGAR.",
                schedule="interval:1h"
            ),
            PipelineConfig(
                id="social_sentiment_aggregator",
                name="Social Sentiment Aggregator",
                description="Aggregates mentions from Reddit/Twitter/StockTwits.",
                schedule="interval:15m"
            ),
            PipelineConfig(
                id="news_spider",
                name="Global News Spider",
                description="Crawls major financial news outlets for breaking news.",
                schedule="interval:5m"
            )
        ]
        for p in defaults:
            self.pipelines[p.id] = p
            self.runs[p.id] = []

    def list_pipelines(self) -> List[PipelineConfig]:
        return list(self.pipelines.values())

    def get_pipeline(self, pipeline_id: str) -> Optional[PipelineConfig]:
        return self.pipelines.get(pipeline_id)

    def get_pipeline_runs(self, pipeline_id: str, limit: int = 10) -> List[PipelineRun]:
        return sorted(
            self.runs.get(pipeline_id, []), 
            key=lambda x: x.start_time, 
            reverse=True
        )[:limit]

    async def trigger_pipeline(self, pipeline_id: str, params: Dict = None) -> str:
        if pipeline_id not in self.pipelines:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        pipeline = self.pipelines[pipeline_id]
        if pipeline.status == "running":
            raise RuntimeError(f"Pipeline {pipeline_id} is already running")

        run_id = f"run_{int(datetime.now().timestamp())}"
        run = PipelineRun(
            run_id=run_id,
            pipeline_id=pipeline_id,
            status="running",
            start_time=datetime.now()
        )
        self.runs[pipeline_id].append(run)
        pipeline.status = "running"
        pipeline.last_run = datetime.now()

        # Simulate async execution (placeholder for actual logic)
        asyncio.create_task(self._execute_pipeline_mock(pipeline_id, run_id))
        
        return run_id

    async def _execute_pipeline_mock(self, pipeline_id: str, run_id: str):
        logger.info(f"Starting mock execution for {pipeline_id} run {run_id}")
        await asyncio.sleep(5)  # Simulate work
        
        # Update run status
        pipeline = self.pipelines[pipeline_id]
        runs = self.runs[pipeline_id]
        current_run = next((r for r in runs if r.run_id == run_id), None)
        
        if current_run:
            current_run.end_time = datetime.now()
            current_run.duration_ms = (current_run.end_time - current_run.start_time).total_seconds() * 1000
            current_run.status = "success"
            current_run.logs.append("Pipeline executed successfully.")
        
        pipeline.status = "idle"
        logger.info(f"Finished mock execution for {pipeline_id}")

    def update_pipeline(self, pipeline_id: str, updates: Dict) -> PipelineConfig:
        if pipeline_id not in self.pipelines:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        pipeline = self.pipelines[pipeline_id]
        for key, value in updates.items():
             if hasattr(pipeline, key):
                 setattr(pipeline, key, value)
        
        return pipeline
