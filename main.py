from fastapi import FastAPI
from annotator import Annotator
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

annotator = Annotator()
app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins)

@app.post('/annotate_text')
def annotate_text(text: str):
    return JSONResponse(annotator.annotate(text))

@app.get('/', status_code=200)
async def healthcheck():
    return 'Annotator is ready!'