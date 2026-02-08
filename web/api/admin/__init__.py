from fastapi import APIRouter
from .event_bus_api import router as event_bus_router
from .cache_api import router as cache_router
from .kafka_api import router as kafka_router
from .storage_api import router as storage_router
from .graph_api import router as graph_router
from .logs_api import router as logs_router
from .health_api import router as health_router
from .latency_api import router as latency_router
from .websocket_api import router as ws_router
from .middleware_api import router as middleware_router
from .alert_api import router as alert_router
from .deployments_api import router as deployments_router

router = APIRouter(prefix="/api/v1/admin")
router.include_router(event_bus_router)
router.include_router(cache_router)
router.include_router(kafka_router)
router.include_router(storage_router)
router.include_router(graph_router)
router.include_router(logs_router)
router.include_router(health_router)
router.include_router(latency_router)
router.include_router(ws_router)
router.include_router(middleware_router)
router.include_router(alert_router)
router.include_router(deployments_router)

from .ops_api import router as ops_router
router.include_router(ops_router)

from .workspaces_api import router as workspaces_router
router.include_router(workspaces_router)

from .env_api import router as env_router
router.include_router(env_router)

from .features_api import router as features_router
router.include_router(features_router)
