
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from models import Item
from strategys.function import get_symbol_info, dataFrame_day
import concurrent.futures

router = APIRouter(
    prefix="/symbols",
)


# symbols_info를 return 함
@router.get("/symbols_info", response_class=JSONResponse)
async def symbols_info():
    symbols = ["ETH", "BTC", "XRP", "DOGE", "SOL", 
                "STX", "BNB", "TRX", "LINK", "NEO",
                "SXP", "ATOM", "XLM", "KAS", "TON"]
    symbols = [symbol+"/USDT" for symbol in symbols]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 병렬로 dataFrame_day 함수를 호출합니다.
        dataframes = list(executor.map(dataFrame_day, symbols))

    data = {}
    for symbol, df in zip(symbols, dataframes):
        cur_price, daily_per = get_symbol_info(symbol, df)
        data[f"{symbol.split('/')[0]}_cur_price"] = cur_price
        data[f"{symbol.split('/')[0]}_daily_per"] = daily_per

    return JSONResponse(content=data)