from groq import Groq
import os
import json
from django.conf import settings

try:
    # Get API key from Django settings or environment
    GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', os.getenv('GROQ_API_KEY'))
    
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment variables or Django settings")
        
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

def generate_product_description(product_name):
    if not client:
        return "AI description service is currently unavailable. Please check the API key configuration."
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",       # New recommended model
            messages=[
                {
                    "role": "system",
                    "content": "You are a product description generator for an inventory management system. Generate concise, engaging product descriptions in JSON format with a 'description' key."
                },
                {
                    "role": "user",
                    "content": f"Generate a 2-3 sentence product description for: {product_name}"
                }
            ],
            temperature=0.7,
            max_tokens=150,
            response_format={"type": "json_object"},
        )
        
        try:
            response = json.loads(completion.choices[0].message.content)
            return response.get("description", "No description generated")
        except json.JSONDecodeError:
            return completion.choices[0].message.content
            
    except Exception as e:
        print(f"Error generating description: {e}")
        return f"Failed to generate description: {str(e)}"