from fastapi import FastAPI
from annotator import Annotator
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel


annotator = Annotator()
app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins)

class Text(BaseModel):
    text: str

@app.post('/annotate_text')
def annotate_text(text: Text):
    return JSONResponse(annotator.annotate(text.text))

@app.get('/', status_code=200)
async def healthcheck():
    return 'Annotator is ready!'