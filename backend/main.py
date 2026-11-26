from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.controller import ALRoute, PLRoute

from app.controller import ASERoute, MASERoute, AERoute, OMAERoute

from app.controller import ASRoute, PSRoute

from app.controller import AORoute, MAORoute

from app.controller import ATCRoute, MATCRoute, ACRoute, MACRoute

from app.controller import URoute, DURoute, RRoute, ORDERoute

from app.controller import ASPRouter, MSPRouter, AMPYRouter, MMPRouter, APAYRouter, MPAYRouter

from app.controller import ASNRouter, ANRoute, ACNRoute, ACANRoute

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(os.getenv("HOST"))],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

""""Публичные маршруты"""
app.include_router(URoute)
app.include_router(PLRoute)
app.include_router(PSRoute)

""""Защищенные маршруты"""
app.include_router(DURoute)
app.include_router(ORDERoute)

"""Админ маршруты"""
app.include_router(ACRoute)
app.include_router(AORoute)
app.include_router(ASRoute)
app.include_router(ALRoute)
app.include_router(AERoute)
app.include_router(ASERoute)
app.include_router(ATCRoute)
app.include_router(RRoute)
app.include_router(ASPRouter)
app.include_router(AMPYRouter)
app.include_router(APAYRouter)
app.include_router(ASNRouter)
app.include_router(ANRoute)
app.include_router(ACNRoute)
app.include_router(ACANRoute)

""""Менеджер маршруты"""
app.include_router(MAORoute)
app.include_router(OMAERoute)
app.include_router(MATCRoute)
app.include_router(MASERoute)
app.include_router(MACRoute)
app.include_router(MSPRouter)
app.include_router(MMPRouter)
app.include_router(MPAYRouter)

@app.get("/")
async def root():
    return {"messege": "Приложкние запущено"}
