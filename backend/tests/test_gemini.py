import pytest
from unittest.mock import AsyncMock, patch
from gemini_service import GeminiService

@pytest.mark.asyncio
async def test_gemini_demo_fallback():
    # Force use_gemini to False to test fallback logic
    service = GeminiService()
    service.use_gemini = False
    
    mock_live_data = {
        "summary": {"busiest_zone": "Gate 1", "avg_food_wait": 5},
        "sim_time": {"display": "18:00"},
        "phase": "pre_match"
    }
    
    response = await service.chat("Where is the food?", mock_live_data, "English")
    assert len(response) > 0
    assert "food" in response.lower() or "wait" in response.lower() or "minute" in response.lower()

@pytest.mark.asyncio
@patch("gemini_service.model")
async def test_gemini_api_call(mock_model):
    service = GeminiService()
    service.use_gemini = True
    service.api_key = "fake_key"
    
    mock_response = AsyncMock()
    mock_response.text = "This is a mocked AI response"
    mock_model.generate_content_async.return_value = mock_response
    
    response = await service.chat("Test message", {}, "English")
    assert response == "This is a mocked AI response"
    mock_model.generate_content_async.assert_called_once()
