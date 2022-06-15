#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importing libraries
from fastapi import FastAPI, Request, Query, Path
import os
import time
from fastapi.templating import Jinja2Templates
import jwt



dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory path

templates_path = f'{dir_path}/templates'
templates = Jinja2Templates(directory=templates_path)

METABASE_SITE_URL = "http://analitica.globalwork.co"
METABASE_SECRET_KEY = "17b1325e3daf5c3234e726219873ce67e2c3684f54a126fbddd2eb83ea801958"

app = FastAPI()

def get_token(payload):
    return jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")


@app.get('/clients/{client_id}')
def get_dashboard(request: Request,
                client_id: int = Path(title="The client ID", default=130),
                month_date :str = Query(title="Query month", regex="^[0-9]{4}-[0-9]{2}$", default='2022-01')):

  payload = {
  "resource": {"dashboard": 30},
  "params": {
    "id_del_cliente": client_id,
    "mes": month_date
  },
  "exp": round(time.time()) + (60 * 10) # 10 minute expiration
    }


  iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + get_token(payload) + "#bordered=false&titled=false"
  return templates.TemplateResponse("base.html", {"request": request,
                                                  "iframeUrl": iframeUrl})
