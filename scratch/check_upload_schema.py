from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional, Annotated
import json

app = FastAPI()

@app.post("/upload")
async def upload_pdf(
    files: Annotated[List[UploadFile], File()], 
    session_id: Annotated[Optional[str], Form()] = None
):
    pass

schema = app.openapi()
print(json.dumps(schema["components"]["schemas"]["Body_upload_pdf_upload_post"], indent=2))
