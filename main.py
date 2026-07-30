from fastapi import FastAPI

app = FastAPI(
    title="JobPilot AI",
    version="0.1.0",
    description="La plataforma inteligente para ayudar a las personas a encontrar empleo."
)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a JobPilot AI 🚀",
        "version": "0.1.0",
        "estado": "API funcionando correctamente"
    }