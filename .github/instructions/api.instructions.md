---
applyTo: "**"
---

# LiberGPT Copilot API Documentation

## Overview

The LiberGPT Copilot API provides access to an AI-powered assistant service that can answer questions and provide explanations on various topics. This API is used by the UG Exam Copilot userscript to automatically answer exam questions.

## Base Information

- **Base URL**: `https://api.zpi.my.id/v1/ai/copilot`
- **Protocol**: HTTPS
- **Method**: POST
- **Content Type**: application/json
- **Rate Limiting**: Not specified (use responsibly)

## Authentication

**No authentication required** - The API is publicly accessible.

## Endpoint

### POST /v1/ai/copilot

Sends a prompt to the AI assistant and receives a response.

#### Request Format

```
POST https://api.zpi.my.id/v1/ai/copilot
Content-Type: application/json
```

#### Request Body

The request body should be a JSON object with the following structure:

```json
{
  "stream": "false",
  "messages": [
    {"role": "system", "content": "You are LiberGPT"},
    {"role": "user", "content": "Your question or prompt here"}
  ]
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `stream` | string | Yes | Set to "false" for non-streaming responses |
| `messages` | array | Yes | Array of message objects representing the conversation |
| `messages[].role` | string | Yes | Role of the message sender ("system" or "user") |
| `messages[].content` | string | Yes | Content of the message |

#### Request Headers

```http
Accept: application/json
Content-Type: application/json
User-Agent: [Your application identifier]
```

## Response Format

### Success Response

**HTTP Status**: `200 OK`

**Content-Type**: `application/json`

```json
{
  "code": 200,
  "response": {
    "provider": "microsoft",
    "content": "AI-generated response text here...",
    "messages": [
      {"role": "system", "content": "You are LiberGPT"},
      {"role": "user", "content": "Your question"},
      {"role": "assistant", "content": "AI-generated response text here..."}
    ]
  }
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `code` | number | HTTP status code (always 200 for successful requests) |
| `response` | object | Container for the AI response |
| `response.provider` | string | AI provider identifier (e.g., "microsoft") |
| `response.content` | string | The actual AI-generated text response |
| `response.messages` | array | Complete conversation history including the new response |

### Error Response

**HTTP Status**: `4xx` or `5xx` (varies based on error type)

**Content-Type**: `application/json`

```json
{
  "error": "Error description",
  "code": 400,
  "message": "Detailed error message"
}
```

## Usage Examples

### JavaScript (Browser/Userscript)

```javascript
/**
 * Fetches AI response using the LiberGPT Copilot API
 * @param {string} prompt - The question or prompt to send
 * @returns {Promise<string>} The AI response content
 */
async function fetchAIResponse(prompt) {
    try {
        const payload = {
            stream: "false",
            messages: [
                { role: "system", content: "You are LiberGPT" },
                { role: "user", content: prompt }
            ]
        };
        
        const response = await fetch('https://api.zpi.my.id/v1/ai/copilot', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.code === 200 && data.response && data.response.content) {
            return data.response.content;
        } else {
            throw new Error('Unexpected response format');
        }
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Usage
fetchAIResponse("What is machine learning?")
    .then(response => console.log(response))
    .catch(error => console.error(error));
```

### Python

```python
import requests
import json

def get_ai_response(prompt: str) -> str:
    """
    Fetches AI response using the LiberGPT Copilot API
    
    Args:
        prompt (str): The question or prompt to send
        
    Returns:
        str: The AI response content
        
    Raises:
        Exception: If the API request fails or returns unexpected format
    """
    try:
        # Prepare payload
        payload = {
            "stream": "false",
            "messages": [
                {"role": "system", "content": "You are LiberGPT"},
                {"role": "user", "content": prompt}
            ]
        }
        
        # Make request
        response = requests.post(
            "https://api.zpi.my.id/v1/ai/copilot",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        if data.get("code") == 200 and data.get("response", {}).get("content"):
            return data["response"]["content"]
        else:
            raise Exception("Unexpected response format")
            
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"API error: {str(e)}")

# Usage
try:
    response = get_ai_response("Explain Python programming")
    print(response)
except Exception as e:
    print(f"Error: {e}")
```

### cURL

```bash
# Basic request
curl -X POST "https://api.zpi.my.id/v1/ai/copilot" \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "stream": "false",
       "messages": [
         {"role": "system", "content": "You are LiberGPT"},
         {"role": "user", "content": "Hello! What is AI?"}
       ]
     }'

# With proper error handling
curl -X POST "https://api.zpi.my.id/v1/ai/copilot" \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "stream": "false",
       "messages": [
         {"role": "system", "content": "You are LiberGPT"},
         {"role": "user", "content": "Hello! What is AI?"}
       ]
     }' \
     -w "HTTP Status: %{http_code}\n" \
     -s -S
```

## Response Examples

### Successful Response

**Request**: 
```json
{
  "stream": "false",
  "messages": [
    {"role": "system", "content": "You are LiberGPT"},
    {"role": "user", "content": "What is Python programming?"}
  ]
}
```

**Response**:
```json
{
  "code": 200,
  "response": {
    "provider": "microsoft",
    "content": "Of course! **Python** is a popular programming language that's known for being easy to learn and use. Think of it like a set of instructions you give to a computer to make it do things—whether that's building a website, analyzing data, or even controlling a robot.\n\nIt's great for beginners because the way you write Python code is more like plain English compared to some other programming languages. Plus, it's used by big companies like Google and Netflix, so learning it can open a lot of doors!\n\nWould you like an example of what Python code looks like?",
    "messages": [
      {"role": "system", "content": "You are LiberGPT"},
      {"role": "user", "content": "What is Python programming?"},
      {"role": "assistant", "content": "Of course! **Python** is a popular programming language that's known for being easy to learn and use. Think of it like a set of instructions you give to a computer to make it do things—whether that's building a website, analyzing data, or even controlling a robot.\n\nIt's great for beginners because the way you write Python code is more like plain English compared to some other programming languages. Plus, it's used by big companies like Google and Netflix, so learning it can open a lot of doors!\n\nWould you like an example of what Python code looks like?"}
    ]
  }
}
```

### Error Response Example

**Request**: Invalid or malformed request

**Response**:
```json
{
  "code": 400,
  "error": "Bad Request",
  "message": "Invalid or missing 'text' parameter"
}
```
