#!/bin/bash

# Example curl command to test the /voice endpoint with a fake SpeechResult
# Replace the URL with your actual server URL (e.g., ngrok URL)

curl -X POST "http://localhost:5050/voice" \
  -H "Content-Type: application/json" \
  -d '{
    "SpeechResult": "What are your hours today?",
    "Confidence": 0.95,
    "CallSid": "test_call_123",
    "From": "+1234567890",
    "To": "+0987654321"
  }'

echo ""
echo "Expected response: Restaurant hours information"
