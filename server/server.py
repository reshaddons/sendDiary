from touch import touch
from fastapi import Depends, FastAPI, Request
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import aiogram
import uvicorn

from typing import Union
from datetime import datetime
import hashlib
import os
import json

load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=os.getenv("FASTAPI_BEARER"))
bot = aiogram.client.bot.Bot(os.getenv('TG_TOKEN'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/update")
async def update_resh(req: Request, token: str = Depends(oauth2_scheme)):
    js = await req.json()
    data = js['data']
    data_sub = {}
    data_real = ''
    for item in json.loads(data):
        key = item.split(' @ ')[0].strip()
        if key not in data_sub:
            data_sub[key] = ''
        data_sub[key] += item.split(' @ ')[1].strip()+'\n'
    for item in list(data_sub.keys()):
        data_real += f'{item}\n{data_sub[item]}\n'
    date = datetime.now().strftime('%H:%M %d.%m.%Y')
    text = f'{data_real}Обновлено: {date}'
    if not os.path.exists('.hash'):
       touch('.hash')
    if not os.path.exists('.last_message_id'):
       touch('.last_message_id')
    with open('.hash', encoding='utf8') as f:
        hash = f.read()
    if hashlib.md5(data.encode()).hexdigest() == hash:
        return {'updated': False}
    with open('.hash', 'w+', encoding='utf8') as f:
        f.write(hashlib.md5(data.encode()).hexdigest())
    newmid = None
    with open('.last_message_id') as f:
        mid = f.read()
        if mid != '':
            await bot.edit_message_text(text, int(os.getenv('TG_CHATID')), mid)
        else:
            newmid = (await bot.send_message(int(os.getenv('TG_CHATID')), text)).message_id
    if newmid:
        with open('.last_message_id','w+') as f:
            f.write(str(newmid))
    return {'updated': True}

uvicorn.run(app, port=int(os.getenv('FASTAPI_PORT')), host=os.getenv('FASTAPI_HOST'), ssl_keyfile=os.getenv('SSL_KEY'), ssl_certfile=os.getenv('SSL_CERT'))
