from fastapi import FastAPI
import uvicorn

from app.routers import news, summary

# app = FastAPI()

app = FastAPI(
    title="News Summary API",
    version="0.2",
    description="This is an news scrapping API",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Bhagyasree Sarker",
        #"url": "https://growwithdata.net",
        "email": "bhagyasreesarker@gmail.com",
    },
    # license_info = {
    #     "name": "MIT License",
    #     "url": "https://opensource.org/licenses/MIT",
    # },
    redoc_url="/documentation",
    docs_url="/try-out",
)

app.include_router(news.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Summary API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
    #uvicorn.run("main:app", host="localhost", port=8011, reload=True)