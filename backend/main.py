from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from strategys.init import binance
from strategys.position import enter_position, exit_position
from strategys.function import get_cur_price, get_balance, dataFrame, calAmount, VolatilityBreakout
from strategys.env import profit_percent, loss_percent, purchase_percent, con_diffma40_4, timeframe, symbols, k
from strategys.strategy import strategy_1, strategy_2, strategy_3


from pydantic import BaseModel
from typing import Dict
import datetime


from domain.history import history_router
from domain.symbols import symbols_router
from domain.user import user_router
app = FastAPI()


# Add CORS middleware
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 입력 양식
class Enter_info(BaseModel):
    strategy : str
    symbol : str
    purchase_percent : float
    leverage : int

@app.get("/")
async def init(request: Request):
    return {"message":"home"}

import uuid
tasks = {}

def position(task_id: str, strategys, symbol, purchase_percent, leverage):
    if strategys == "strategy_1":
        strategy_1(tasks, task_id, symbol, purchase_percent, leverage)
    elif strategys == "strategy_2":
        strategy_2(tasks, task_id, symbol, purchase_percent, leverage)
    elif strategys == "strategy_3":
        strategy_3(tasks, task_id, symbol, purchase_percent, leverage)

@app.post("/enter_position")
async def enter_position(enter_info: Enter_info, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = True
    print(task_id)
    background_tasks.add_task(position, task_id, enter_info.strategy, enter_info.symbol, enter_info.purchase_percent, enter_info.leverage)
    return {"task_id": task_id, **enter_info.dict()}

@app.post("/stop_position")
async def stop_position(task_id: str = Query(...)):
    print("stop : ", task_id)
    if task_id in tasks:
        del tasks[task_id]
        return {"message": "Task stopped successfully"}
    raise HTTPException(status_code=404, detail="Task not found")



app.include_router(history_router.router, tags=["history"])
app.include_router(symbols_router.router, tags=["symbols"])
app.include_router(user_router.router, tags=["user"])