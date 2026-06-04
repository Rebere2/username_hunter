import asyncio
import httpx
from typing import Dict, Any
from jsonpath_ng import parse
import json

from hunter.utils import get_random_user_agent

async def check_platform(
    username: str, 
    platform: Dict[str, Any], 
    client: httpx.AsyncClient,
    strict_mode: bool = False
) -> Dict[str, Any]:
    url = platform["url"].format(username=username)
    method = platform.get("method", "status_code")
    
    headers = {"User-Agent": get_random_user_agent()}
    max_retries = 2
    
    for attempt in range(max_retries + 1):
        try:
            # Léger délai pour ne pas surcharger
            await asyncio.sleep(0.1)
            response = await client.get(url, headers=headers, follow_redirects=True)
            
            status = "NOT_FOUND"
            
            if method == "status_code":
                if response.status_code == platform.get("found_code", 200):
                    status = "FOUND"
                    
                # Mode strict: vérification additionnelle
                if strict_mode and status == "FOUND":
                    text = response.text.lower()
                    if "not found" in text or "doesn't exist" in text or "404" in text:
                        status = "NOT_FOUND"
                        
            elif method == "body_text":
                found_str = platform.get("found_string", "")
                not_found_str = platform.get("not_found_string", "")
                
                if found_str and found_str in response.text:
                    status = "FOUND"
                elif not_found_str and not_found_str in response.text:
                    status = "NOT_FOUND"
                    
            elif method == "json_field":
                try:
                    data = response.json()
                    jsonpath_expr = parse(platform.get("found_path", ""))
                    match = jsonpath_expr.find(data)
                    if match:
                        status = "FOUND"
                except json.JSONDecodeError:
                    pass

            return {
                "platform": platform["name"],
                "url": url,
                "status": status,
                "response_time": response.elapsed.total_seconds()
            }
            
        except httpx.RequestError as e:
            if attempt < max_retries:
                await asyncio.sleep(2 ** attempt)  # Backoff exponentiel
                continue
            return {
                "platform": platform["name"],
                "url": url,
                "status": "ERROR",
                "error": str(e),
                "response_time": 0
            }
            
    return {
        "platform": platform["name"],
        "url": url,
        "status": "ERROR",
        "error": "Max retries exceeded",
        "response_time": 0
    }
