---
applyTo: "**"
---

# LiberGPT Copilot API Documentation

## Overview

The LiberGPT Copilot API provides access to an AI-powered assistant service that can answer questions and provide explanations on various topics. This API is used by the UG Exam Copilot userscript to automatically answer exam questions.

## Base Information

- **Base URL**: `https://api.zpi.my.id/v1/ai/copilot`
- **CORS Proxy**: `https://cors.fadel.web.id/` (required for browser requests)
- **Protocol**: HTTPS
- **Method**: GET
- **Content Type**: JSON
- **Rate Limiting**: Not specified (use responsibly)

## Authentication

**No authentication required** - The API is publicly accessible.

## Endpoint

### GET /v1/ai/copilot

Sends a prompt to the AI assistant and receives a response.

#### Request Format

```
GET https://cors.fadel.web.id/https://api.zpi.my.id/v1/ai/copilot?text={encoded_prompt}
```

#### Parameters

| Parameter | Type   | Required | Description                                                   |
|-----------|--------|----------|---------------------------------------------------------------|
| `text`    | string | Yes      | The prompt/question to send to the AI (URL-encoded required) |

#### URL Encoding

**Important**: The `text` parameter must be properly URL-encoded to handle special characters, spaces, and punctuation.

**Examples**:
- Input: `Hello! Can you explain what Python is?`
- Encoded: `Hello%21%20Can%20you%20explain%20what%20Python%20is%3F`

#### Request Headers

```http
Accept: application/json
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
    "content": "AI-generated response text here..."
  }
}
```

#### Response Fields

| Field             | Type   | Description                                           |
|-------------------|--------|-------------------------------------------------------|
| `code`            | number | HTTP status code (always 200 for successful requests)|
| `response`        | object | Container for the AI response                         |
| `response.content`| string | The actual AI-generated text response                 |

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
        const encodedPrompt = encodeURIComponent(prompt);
        const baseEndpoint = 'https://api.zpi.my.id/v1/ai/copilot';
        const fullUrl = `${baseEndpoint}?text=${encodedPrompt}`;
        const proxiedUrl = `https://cors.fadel.web.id/${fullUrl}`;
        
        const response = await fetch(proxiedUrl);
        
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
import urllib.parse

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
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Construct URL
        base_endpoint = "https://api.zpi.my.id/v1/ai/copilot"
        full_url = f"{base_endpoint}?text={encoded_prompt}"
        proxied_url = f"https://cors.fadel.web.id/{full_url}"
        
        # Make request
        response = requests.get(proxied_url)
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
curl -X GET "https://cors.fadel.web.id/https://api.zpi.my.id/v1/ai/copilot?text=Hello%21%20What%20is%20AI%3F" \
     -H "Accept: application/json"

# With proper error handling
curl -X GET "https://cors.fadel.web.id/https://api.zpi.my.id/v1/ai/copilot?text=Hello%21%20What%20is%20AI%3F" \
     -H "Accept: application/json" \
     -w "HTTP Status: %{http_code}\n" \
     -s -S
```

## Response Examples

### Successful Response

**Request**: `What is Python programming?`

**Response**:
```json
{
  "code": 200,
  "response": {
    "content": "Of course! **Python** is a popular programming language that's known for being easy to learn and use. Think of it like a set of instructions you give to a computer to make it do things—whether that's building a website, analyzing data, or even controlling a robot.\n\nIt's great for beginners because the way you write Python code is more like plain English compared to some other programming languages. Plus, it's used by big companies like Google and Netflix, so learning it can open a lot of doors!\n\nWould you like an example of what Python code looks like?"
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
