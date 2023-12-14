from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI


class Prompt(BaseModel):
    ori_prompt: str

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "I am alive."}


@app.post("/prompt_util")
async def handle_request(prompt: Prompt):
    prompt_dict = prompt.dict()
    ori_prompt = prompt_dict["ori_prompt"]

    # new_prompt = process_prompt(old_prompt)
    new_prompt = f'hhhh'

    return {"new_prompt": new_prompt}
