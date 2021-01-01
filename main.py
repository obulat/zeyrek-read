from fastapi import FastAPI
from annotator import Annotator
from starlette.responses import JSONResponse

annotator = Annotator()
app = FastAPI()

@app.post('/annotate_text')
def annotate_text(text: str):
    return JSONResponse(annotator.annotate(text))

@app.get('/', status_code=200)
async def healthcheck():
    return 'Annotator is ready!'