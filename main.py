import requests
import json


class OpenAPIAnalyzer:
    def __init__(self, spec):
        self.spec = spec

    def analyze(self):
        return {
            "api_info": self.get_api_info(),
            "openapi_version": self.get_openapi_version(),
            "endpoints": self.get_endpoints(),
            "schemas": self.get_schemas(),
            "security": self.get_security(),
            "servers": self.get_servers()
        }

    def get_api_info(self):
        info = self.spec.get("info", {})
        return {
            "title": info.get("title"),
            "version": info.get("version"),
            "description": info.get("description")
        }

    def get_openapi_version(self):
        return self.spec.get("openapi")

    def get_endpoints(self):
        paths = self.spec.get("paths", {})
        endpoints = []
        for path, methods in paths.items():
            for method, details in methods.items():
                endpoints.append({
                    "path": path,
                    "method": method,
                    "summary": details.get("summary"),
                    "operationId": details.get("operationId"),
                    "parameters": details.get("parameters", []),
                    "responses": details.get("responses", {})
                })
        return endpoints

    def get_schemas(self):
        return self.spec.get("components", {}).get("schemas", {})

    def get_security(self):
        return self.spec.get("security", [])

    def get_servers(self):
        return self.spec.get("servers", [])


def get_openapi_spec_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching OpenAPI specification: {e}")
        return None
    except json.JSONDecodeError:
        print("The response from the URL is not valid JSON.")
        return None


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

    analyzer = OpenAPIAnalyzer(spec)
    analysis = analyzer.analyze()

    for key, value in analysis.items():
        print(f"\n{key}:")
        print(json.dumps(value, indent=2))

if __name__ == "__main__":
    main()