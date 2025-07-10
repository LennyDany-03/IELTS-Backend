from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.essay_router import essay_router
from routers.speech_router import speech_router
from routers.reading_router import router as reading_router
from routers.listening_router import router as listening_router  # ✅ New import

app = FastAPI()

# ✅ CORS setup
origins = [
    "https://ielts-project-gilt.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ No paths, just domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Mount routers with clear prefixes
app.include_router(essay_router, prefix="/api/essay", tags=["Essay"])
app.include_router(speech_router, prefix="/api/speech", tags=["Speech"])
app.include_router(reading_router)
app.include_router(listening_router)

