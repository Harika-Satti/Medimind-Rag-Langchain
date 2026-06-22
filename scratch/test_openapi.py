import sys
import os
from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional, Annotated

app = FastAPI()

@app.post("/upload")
async def upload_pdf(
    files: Annotated[List[UploadFile], File()],
    session_id: Annotated[Optional[str], Form()] = None
):
    return {"filenames": [f.filename for f in files]}

# Inspect the OpenAPI schema
import json
print(json.dumps(app.openapi(), indent=2))
