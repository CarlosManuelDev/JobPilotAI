import requests

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "prueba_final@jobpilotai.com"
PASSWORD = "clave12345"

print("PASO 1: Registrando usuario...")
r1 = requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": EMAIL, "password": PASSWORD, "full_name": "Prueba Final",
    "country": "Republica Dominicana", "preferred_language": "es",
})
print(r1.status_code, r1.json())

print("\nPASO 2: Iniciando sesión...")
r2 = requests.post(f"{BASE_URL}/api/auth/login", data={
    "username": EMAIL, "password": PASSWORD,
})
print(r2.status_code, r2.json())