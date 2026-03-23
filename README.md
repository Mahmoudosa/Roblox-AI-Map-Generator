# 🗺️ Roblox AI Map Generator

Built by **Mahmoud Obeidat** — CS Student at 3th Year

## 🚀 What is this?
An AI-powered tool that generates Roblox 3D maps from a text description.
Type "konoha village" or "small city" and the AI builds it for you inside Roblox.

## 🎮 Demo
- User types a map description in the UI
- AI generates a structured layout
- Roblox spawns the map in real time
- Player can walk around the generated map

## 🛠️ How it works
1. User types description in Roblox UI
2. Lua script sends request to FastAPI backend
3. FastAPI sends two prompts to Groq AI:
   - **Prompt 1** — Plan the map layout (zones and positions)
   - **Prompt 2** — Convert layout into 3D Roblox parts
4. JSON response is parsed and parts are spawned in Roblox

## 💻 Tech Stack
- **Python** + **FastAPI** — Backend API
- **Groq API** — AI model (llama-3.1)
- **Lua** — Roblox game scripting
- **ngrok** — Expose local server to Roblox

## ⚙️ How to run
1. Clone the repo
2. Install dependencies:
```
pip install fastapi uvicorn groq
```
3. Set your Groq API key:
```
export GROQ_API_KEY=your_key_here
```
4. Run the server:
```
uvicorn main:app --reload
```
5. Run ngrok:
```
ngrok http 8000
```
6. Update the ngrok URL in the Roblox Lua script
7. Press Play in Roblox Studio

## 📌 Note
This is an MVP project built to learn FastAPI, AI APIs, and Roblox game development.
