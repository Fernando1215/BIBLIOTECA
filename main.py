from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Crear la aplicación
app = FastAPI(title="Sistema Biblioteca FastAPI")

# Página HTML principal
HTML_PAGE = """ 
<!DOCTYPE html>
<html>
<head>
    <title>📚 Sistema Biblioteca</title>
    <style>
        body {
            background-color: #f7f7f7;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 40px;
        }
        h1 {
            color: #333333;
        }
        p {
            color: #555555;
        }
        .card {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            max-width: 500px;
            margin: 40px auto;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
        }
        .footer {
            margin-top: 30px;
            color: gray;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>📚 Bienvenido al Sistema Biblioteca</h1>
        <p>Aplicación desplegada con FastAPI y Azure App Service</p>
    </div>
    <div class="footer">
        <p>Desarrollado por Fernando Caraballo</p>
    </div>
</body>
</html>
"""

# Ruta principal
@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(HTML_PAGE)

# 💚 Ruta para comprobación de estado (Health Check de Azure)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Ejecutar con Uvicorn (para desarrollo local o Azure)
if __name__ == "__main__":
    import uvicorn, os
    puerto = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=puerto)
