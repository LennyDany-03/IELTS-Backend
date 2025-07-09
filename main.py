from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.essay_router import essay_router
from routers.speech_router import speech_router

app = FastAPI()

# ✅ CORS setup
origins = [
    "http://localhost:3000",  # Essay frontend (React/Vite)
    "http://localhost:3001",  # Speech frontend
    # You can add deployed domains here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount routers with clear prefixes
app.include_router(essay_router, prefix="/api/essay", tags=["Essay"])
app.include_router(speech_router, prefix="/api/speech", tags=["Speech"])
