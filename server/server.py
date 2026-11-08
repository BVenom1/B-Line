'''
This is the file where the FastAPI app and endpoints are defined.
'''

# create API application
from fastapi import FastAPI

app = FastAPI()

# create API endpoints
@app.get("/test")
async def test():
    return "this is a test"