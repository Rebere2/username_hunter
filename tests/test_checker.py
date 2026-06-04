import pytest
import respx
import httpx
from hunter.checker import check_platform

@pytest.mark.asyncio
@respx.mock
async def test_check_platform_status_code_found():
    platform = {
        "name": "TestPlatform",
        "url": "https://test.com/{username}",
        "method": "status_code",
        "found_code": 200
    }
    respx.get("https://test.com/johndoe").respond(status_code=200)
    
    async with httpx.AsyncClient() as client:
        result = await check_platform("johndoe", platform, client)
        
    assert result["status"] == "FOUND"
    assert result["platform"] == "TestPlatform"

@pytest.mark.asyncio
@respx.mock
async def test_check_platform_status_code_not_found():
    platform = {
        "name": "TestPlatform",
        "url": "https://test.com/{username}",
        "method": "status_code",
        "found_code": 200
    }
    respx.get("https://test.com/johndoe").respond(status_code=404)
    
    async with httpx.AsyncClient() as client:
        result = await check_platform("johndoe", platform, client)
        
    assert result["status"] == "NOT_FOUND"

@pytest.mark.asyncio
@respx.mock
async def test_check_platform_body_text_found():
    platform = {
        "name": "TestPlatform",
        "url": "https://test.com/{username}",
        "method": "body_text",
        "found_string": "User Profile:"
    }
    respx.get("https://test.com/johndoe").respond(status_code=200, text="<html>User Profile: johndoe</html>")
    
    async with httpx.AsyncClient() as client:
        result = await check_platform("johndoe", platform, client)
        
    assert result["status"] == "FOUND"

@pytest.mark.asyncio
@respx.mock
async def test_check_platform_json_field():
    platform = {
        "name": "TestPlatform",
        "url": "https://api.test.com/users/{username}",
        "method": "json_field",
        "found_path": "$.success"
    }
    respx.get("https://api.test.com/users/johndoe").respond(status_code=200, json={"success": True})
    
    async with httpx.AsyncClient() as client:
        result = await check_platform("johndoe", platform, client)
        
    assert result["status"] == "FOUND"
