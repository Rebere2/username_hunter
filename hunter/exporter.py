import json
import os
from datetime import datetime
from typing import List, Dict, Any

def export_results(username: str, results: List[Dict[str, Any]], output_dir: str = "."):
    """Exporte les résultats en JSON et TXT."""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(output_dir, f"{username}_{timestamp}_results.json")
    txt_path = os.path.join(output_dir, f"{username}_{timestamp}_found.txt")
    
    # JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"username": username, "results": results}, f, indent=4, ensure_ascii=False)
        
    # TXT (uniquement les trouvés)
    found_urls = [r["url"] for r in results if r["status"] == "FOUND"]
    if found_urls:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(found_urls) + "\n")
            
    return json_path, txt_path
