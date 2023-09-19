from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mssql+pyodbc://admin:q1w2e3r4@localhost/ProjectJ?driver=ODBC+Driver+17+for+SQL+Server")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
