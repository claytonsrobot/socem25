# socem25/api/__main__.py
def run():
    import uvicorn
    uvicorn.run("socem25.api.main:app", host="127.0.0.1", port=8000, reload=True)