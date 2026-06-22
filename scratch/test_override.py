from app.main import app
import json

schema = app.openapi()
print(f"OpenAPI Version: {schema.get('openapi', 'unknown')}")
upload_schema = schema["paths"]["/upload"]["post"]["requestBody"]["content"]["multipart/form-data"]["schema"]
print(json.dumps(upload_schema, indent=2))

body_schema_name = upload_schema["$ref"].split("/")[-1]
body_schema = schema["components"]["schemas"][body_schema_name]
print(json.dumps(body_schema, indent=2))
