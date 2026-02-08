import pytest
import time
from fastapi.testclient import TestClient
from web.fastapi_gateway import app

client = TestClient(app)

def test_list_jobs():
    response = client.get("/api/v1/admin/ops/jobs")
    assert response.status_code == 200
    jobs = response.json()
    assert isinstance(jobs, list)
    assert len(jobs) >= 4
    # Check for specific mock job
    assert any(j["id"] == "backup_daily" for j in jobs)

def test_trigger_job_success():
    # Trigger backup_daily (system type, success path)
    response = client.post("/api/v1/admin/ops/jobs/backup_daily/trigger")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "success"
    assert result["job_id"] == "backup_daily"
    assert "execution_id" in result

def test_trigger_job_failure():
    # Trigger model_retrain (mocked to fail)
    response = client.post("/api/v1/admin/ops/jobs/model_retrain/trigger")
    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "failed"
    
def test_trigger_invalid_job():
    response = client.post("/api/v1/admin/ops/jobs/invalid_id/trigger")
    assert response.status_code == 404

def test_get_job_history():
    # Trigger a job to ensure history exists
    client.post("/api/v1/admin/ops/jobs/data_sync/trigger")
    
    response = client.get("/api/v1/admin/ops/jobs/data_sync/history")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) > 0
    assert history[0]["job_id"] == "data_sync"
