import pytest
import os
from services.blue_green_service import get_blue_green_service

@pytest.mark.asyncio
async def test_hot_swap_flow(tmp_path):
    svc = get_blue_green_service()
    
    # Setup dummy agent file
    agent_file = tmp_path / "dummy_agent.py"
    agent_file.write_text("print('Old V1')")
    
    new_code = "print('New V2')"
    
    # 1. Hot Swap
    success = await svc.deploy_hot_swap("dummy_agent", new_code, str(agent_file))
    assert success is True
    
    # 2. Verify File Content Updated
    assert agent_file.read_text() == new_code
    
    # 3. Verify Backup Created
    backups = os.listdir(svc.backup_dir)
    assert len(backups) > 0
    assert "dummy_agent" in backups[-1]
