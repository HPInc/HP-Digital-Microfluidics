from __future__ import annotations

import json

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from quantities.timestamp import time_now
from threading import Thread
from aiohttp.web_runner import GracefulExit


class Listener(Thread):
    app: web.Application
    running: bool = False
    
    async def message(self, request: Request) -> Response:
        try:
            body = await request.json()
        except json.JSONDecodeError:
            text = await body.text()
            print(f"Request was not json: {text}")
            return web.json_response(status=400, data = {"error": "bad-request"})
        
        msg = body["message"]
        stamp = time_now().strftime(fmt="%H:%M:%S")
        print(f"OT-2 [{stamp}]: {msg}")
        return web.json_response()
    
    async def exit(self, request: Request) -> Response:
        # try:
        #     body = await request.json()
        # except json.JSONDecodeError:
        #     text = await body.text()
        #     print(f"Request was not json: {text}")
        #     return web.json_response(status=400, data = {"error": "bad-request"})
        print("Shutting down server")
        raise GracefulExit()
    
    def run(self) -> None:
        app = self.app = web.Application()
        app.router.add_post("/message", self.message)
        app.router.add_post("/exit", self.exit)
        print("Launching listener")
        self.running = True
        web.run_app(app,
                    host="0.0.0.0",
                    port=8087)
        self.running = False
        print("Shut down listener")