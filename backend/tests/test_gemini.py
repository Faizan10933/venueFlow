import pytest
from unittest.mock import MagicMock, patch
from gemini_service import GeminiService

@patch('google.generativeai.GenerativeModel')
def test_gemini_response_generation(mock_model):
    """Test that Gemini service correctly interacts with the Google AI SDK."""
    # Setup mock
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "I recommend the North Food Court."
    mock_model.return_value.start_chat.return_value = mock_chat
    
    service = GeminiService()
    state = {"summary": {"busiest_zone": "South Gate"}}
    
    response = service.get_chat_response("Where should I eat?", state)
    
    assert "North Food Court" in response
    assert mock_chat.send_message.called

def test_gemini_prompt_sanitization():
    """Ensure prompt sanitization handles empty or malicious input."""
    service = GeminiService()
    
    # Test short message
    res = service.get_chat_response("a", {})
    assert "ask a more specific question" in res.lower()
