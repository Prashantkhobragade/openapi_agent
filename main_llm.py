
import requests
import json
from langchain_groq import ChatGroq
from groq import Groq
import os


from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.environ["GROQ_API_KEY"]


llm = Groq()

def get_openapi_spec_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching OpenAPI specification: {e}")
        return None
    except json.JSONDecodeError:
        print("The response from the URL is not valid JSON.")
        return None

def analyze_with_llama(spec):
    prompt = f"""
    Analyze the following OpenAPI specification and provide a detailed breakdown:

    {json.dumps(spec, indent=2)}

    Please include information on:
    1. API Info (title, version, description)
    2. OpenAPI version
    3. Endpoints (paths, methods, parameters, responses)
    4. Schemas
    5. Security
    6. Servers
    7. Payload

    Provide a comprehensive analysis with clear headings for each section.
    """

    try:
        response = llm.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert in analyzing OpenAPI specifications."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error in llama3 analysis: {str(e)}"

def get_user_input():
    while True:
        url = input("Please enter the URL of the OpenAPI specification endpoint: ").strip()
        if url:
            return url
        else:
            print("URL cannot be empty. Please try again.")

def main():
    url = get_user_input()
    spec = get_openapi_spec_from_url(url)
    
    if spec is None:
        print("Failed to retrieve a valid OpenAPI specification. Exiting.")
        return

    analysis = analyze_with_llama(spec)
    print("\nAnalysis:")
    print(analysis)

if __name__ == "__main__":
    main()