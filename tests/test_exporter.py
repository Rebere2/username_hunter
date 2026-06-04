import os
import json
from hunter.exporter import export_results

def test_export_results(tmp_path):
    results = [
        {"platform": "Test1", "url": "url1", "status": "FOUND"},
        {"platform": "Test2", "url": "url2", "status": "NOT_FOUND"}
    ]
    
    output_dir = str(tmp_path)
    json_path, txt_path = export_results("testuser", results, output_dir)
    
    assert os.path.exists(json_path)
    assert os.path.exists(txt_path)
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["username"] == "testuser"
        assert len(data["results"]) == 2
        
    with open(txt_path, "r", encoding="utf-8") as f:
        txt = f.read()
        assert "url1" in txt
        assert "url2" not in txt
