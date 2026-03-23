from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()

class bodyrequest(BaseModel):
    description: str

def call_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content.strip()
    if result.startswith("```json"):
        result = result.split("\n", 1)[1]
    if result.startswith("```"):
        result = result.split("\n", 1)[1]
    if result.endswith("```"):
        result = result.rsplit("```", 1)[0]
    return result.strip()

@app.post("/generate")
def generate_map(data: bodyrequest):

    prompt1 = f"""You are given this description: "{data.description}"
Create a map layout as a JSON array. Output ONLY JSON.
Example: [{{"type":"tree","x":30,"z":-40}},{{"type":"house","x":-50,"z":20}}]
Read the description carefully:
- If it says "forest" or "many trees" generate 15+ tree zones
- If it says "big" or "large" set a "scale" field to 2
- If it says "small" set "scale" to 0.5
- Spread all zones between -80 and 80, no clustering
Up to 20 zones."""

    layout = call_groq(prompt1)

    prompt2 = f"""Create a Roblox map from: {layout}
Output ONLY a JSON array, no text, no explanation.
Format: [{{"part":"name","position":[x,y,z],"size":[x,y,z],"color":[r,g,b],"material":"MaterialName","anchored":true,"canCollide":true}}]

EXACT examples you MUST follow. Use "scale" from layout to multiply sizes:

HOUSE at x=20, z=30 scale=1:
{{"part":"wall","position":[20,3.5,30],"size":[8,6,8],"color":[r,g,b],"material":"SmoothPlastic","anchored":true,"canCollide":true}}
{{"part":"roof","position":[20,7.5,30],"size":[9,2,9],"color":[r,g,b],"material":"SmoothPlastic","anchored":true,"canCollide":true}}

HOUSE at x=20, z=30 scale=2 (big house):
{{"part":"wall","position":[20,6.5,30],"size":[16,12,16],"color":[r,g,b],"material":"SmoothPlastic","anchored":true,"canCollide":true}}
{{"part":"roof","position":[20,13.5,30],"size":[18,3,18],"color":[r,g,b],"material":"SmoothPlastic","anchored":true,"canCollide":true}}

TREE at x=-40, z=10 scale=1:
{{"part":"trunk","position":[-40,2.5,10],"size":[1,4,1],"color":[r,g,b],"material":"Wood","anchored":true,"canCollide":true}}
{{"part":"leaves","position":[-40,6.5,10],"size":[4,4,4],"color":[r,g,b],"material":"Grass","anchored":true,"canCollide":true}}

TREE at x=-40, z=10 scale=2 (big tree):
{{"part":"trunk","position":[-40,4.5,10],"size":[2,8,2],"color":[r,g,b],"material":"Wood","anchored":true,"canCollide":true}}
{{"part":"leaves","position":[-40,11.5,10],"size":[8,7,8],"color":[r,g,b],"material":"Grass","anchored":true,"canCollide":true}}

GROUND always first:
{{"part":"ground","position":[0,0,0],"size":[200,1,200],"color":[r,g,b],"material":"Grass","anchored":true,"canCollide":true}}

ROAD at x=0, z=0:
{{"part":"road","position":[0,1,0],"size":[6,1,30],"color":[r,g,b],"material":"Concrete","anchored":true,"canCollide":true}}

Rules:
- Generate ONE part entry per zone from the layout, do not skip any zones
- Use scale from layout to decide sizes, default scale=1
- Replace x and z with exact values from layout: {layout}
- Adapt colors to match theme: "{data.description}"
- No clustering near 0,0"""

    result = call_groq(prompt2)

    try:
        json.loads(result)
    except:
        return {"response": "[]"}

    return {"response": result}