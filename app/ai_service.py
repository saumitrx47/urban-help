import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_service_recommendations(user_query: str, available_services: list) -> str:
    """Get AI-powered service recommendations based on user query"""
    try:
        services_list = "\n".join([f"- {s['name']}: {s['description']}" for s in available_services])
        
        prompt = f"""You are a helpful assistant for a service booking platform. 
        A user is looking for services and asked: "{user_query}"
        
        Available services:
        {services_list}
        
        Provide a helpful recommendation (2-3 sentences) suggesting which service(s) would best match their needs.
        Be friendly and concise."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful service booking assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"I'd be happy to help you find the right service! Please browse our available services above."

