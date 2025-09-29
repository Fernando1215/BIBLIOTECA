# main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Sistema Biblioteca FastAPI")

HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sistema Biblioteca</title>
  <style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
    }
    h1, h2 {
        text-align: center;
        color: #333;
    }
    .container {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    input, select, button {
        display: block;
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
        border: 1px solid #ccc;
        box-sizing: border-box;
    }
    button {
        background-color: #28a745;
        color: white;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    button:hover {
        background-color: #218838;
    }
    #panel, #panelEstudiante, #registro, #detalleLibro {
        display: none;
        margin-top: 20px;
    }
    #catalogo div,
    #catalogoEstudiante div {
        padding: 10px;
        margin: 5px 0;
        background-color: #e9ecef;
        border: 1px solid #ccc;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    #catalogo div:hover,
    #catalogoEstudiante div:hover {
        background-color: #dee2e6;
    }
    .detalle {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 15px;
        margin-top: 10px;
        border-radius: 4px;
    }
    /* 🎨 Botones editar y eliminar */
    #catalogo button {
        display: inline-block;
        width: auto;
        padding: 5px 10px;
        margin-left: 10px;
        border-radius: 4px;
        font-size: 14px;
    }
    #catalogo button:nth-of-type(1) {
        background-color: #007bff;
    }
    #catalogo button:nth-of-type(1):hover {
        background-color: #0069d9;
    }
    #catalogo button:nth-of-type(2) {
        background-color: #dc3545;
    }
  </style>
</head>
<body>
  <div id="login">
    <h2>Ingresar usuario</h2>
    <input type="text" id="usuario" placeholder="Nombre de usuario">
    <input type="password" id="clave" placeholder="Contraseña">
    <button onclick="login()">Ingresar</button>
    <button onclick="mostrarRegistro()">Registrar usuario</button>
  </div>

  <div id="registro">
    <h2>Registrar Usuario</h2>
    <input type="text" id="nuevoNombre" placeholder="Nombre">
    <select id="nuevoRol">
      <option value="estudiante">Estudiante</option>
      <option value="bibliotecario">Bibliotecario</option>
    </select>
    <input type="password" id="nuevaClave" placeholder="Contraseña">
    <button onclick="agregarUsuario()">Registrar</button>
  </div>

  <div id="panel">
    <h2>Panel Bibliotecario</h2>
    <input type="text" id="titulo" placeholder="Título del libro">
    <input type="text" id="autor" placeholder="Autor">
    <input type="text" id="isbn" placeholder="ISBN">
    <input type="text" id="categoria" placeholder="Categoría">
    <input type="number" id="cantidad" placeholder="Cantidad disponible">
    <button onclick="agregarLibro()">Agregar Libro</button>
    <div id="catalogo"></div>
  </div>

  <div id="panelEstudiante">
    <h2>Catálogo de Libros</h2>
    <div id="catalogoEstudiante"></div>
    <h3>Historial de Préstamos</h3>
    <ul id="historialPrestamos"></ul>
  </div>

  <div id="detalleLibro">
    <h3 id="tituloDetalle"></h3>
    <p id="autorDetalle"></p>
    <p id="isbnDetalle"></p>
    <p id="categoriaDetalle"></p>
    <p id="cantidadDetalle"></p>
    <input type="number" id="diasPrestamo" placeholder="Días de préstamo">
    <button onclick="alquilarLibro()">Alquilar</button>
  </div>

  <button id="cerrarSecion" style="display:none;" onclick="logout()">Cerrar sesión</button>

  <script>
    const sheetDB_URL = "https://sheetdb.io/api/v1/0dqfflvb3auk5";
    let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
    let usuarioActual = null;
    let libros = [];
    let historialPrestamos = JSON.parse(localStorage.getItem("historialPrestamos")) || {};
    let libroSeleccionado = null;

    function guardarUsuarios() {
      localStorage.setItem("usuarios", JSON.stringify(usuarios));
      localStorage.setItem("historialPrestamos", JSON.stringify(historialPrestamos));
    }

    function login() {
      const nombre = document.getElementById("usuario").value;
      const clave = document.getElementById("clave").value;
      const user = usuarios.find(u => u.nombre === nombre && u.clave === clave);
      if (!user) { alert("Usuario o clave incorrecta"); return; }
      usuarioActual = user;
      document.getElementById("login").style.display = "none";
      document.getElementById("cerrarSecion").style.display = "block";
      if (user.rol === "bibliotecario") {
        document.getElementById("panel").style.display = "block";
        cargarLibrosDesdeSheets();
      } else {
        document.getElementById("panelEstudiante").style.display = "block";
        cargarLibrosDesdeSheets();
        mostrarHistorial();
      }
    }

    function mostrarRegistro() {
      document.getElementById("registro").style.display = "block";
      document.getElementById("login").style.display = "none";
    }

    function agregarUsuario() {
      const nombre = document.getElementById("nuevoNombre").value;
      const clave = document.getElementById("nuevaClave").value;
      const rol = document.getElementById("nuevoRol").value;
      if (usuarios.some(u => u.nombre === nombre)) { alert("Nombre de usuario ya existe"); return; }
      usuarios.push({ nombre, clave, rol });
      guardarUsuarios();
      alert("Usuario registrado con éxito");
      document.getElementById("registro").style.display = "none";
      document.getElementById("login").style.display = "block";
    }

    function logout() {
      usuarioActual = null;
      document.getElementById("login").style.display = "block";
      document.getElementById("panel").style.display = "none";
      document.getElementById("panelEstudiante").style.display = "none";
      document.getElementById("detalleLibro").style.display = "none";
      document.getElementById("cerrarSecion").style.display = "none";
      document.getElementById("usuario").value = "";
      document.getElementById("clave").value = "";
    }

    async function cargarLibrosDesdeSheets() {
      const response = await fetch(sheetDB_URL);
      const data = await response.json();
      libros = data.map(fila => ({
        titulo: fila.Titulo, autor: fila.Autor, isbn: fila.ISBN,
        categoria: fila.Categoria, cantidad: parseInt(fila.Cantidad) || 0
      }));
      if (usuarioActual.rol === "bibliotecario") { mostrarLibros(); }
      else { mostrarCatalogoEstudiante(); }
    }

    async function agregarLibro() {
      const titulo = document.getElementById("titulo").value;
      const autor = document.getElementById("autor").value;
      const isbn = document.getElementById("isbn").value;
      const categoria = document.getElementById("categoria").value;
      const cantidad = parseInt(document.getElementById("cantidad").value);
      await fetch(sheetDB_URL, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: [{ Titulo: titulo, Autor: autor, ISBN: isbn, Categoria: categoria, Cantidad: cantidad }] })
      });
      alert("Libro agregado ✅"); cargarLibrosDesdeSheets();
    }

    async function editarLibro(isbn) {
      const libro = libros.find(l => l.isbn === isbn);
      const nuevoTitulo = prompt("Nuevo título:", libro.titulo);
      const nuevoAutor = prompt("Nuevo autor:", libro.autor);
      const nuevaCategoria = prompt("Nueva categoría:", libro.categoria);
      const nuevaCantidad = parseInt(prompt("Nueva cantidad:", libro.cantidad));
      if (nuevoTitulo && nuevoAutor && nuevaCategoria && !isNaN(nuevaCantidad)) {
        await fetch(`${sheetDB_URL}/ISBN/${isbn}`, {
          method: "PATCH", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ data: [{ Titulo: nuevoTitulo, Autor: nuevoAutor, Categoria: nuevaCategoria, Cantidad: nuevaCantidad }] })
        });
        alert("Libro editado ✅"); cargarLibrosDesdeSheets();
      }
    }

    async function eliminarLibro(isbn) {
      if (confirm("¿Seguro que deseas eliminar este libro?")) {
        await fetch(`${sheetDB_URL}/ISBN/${isbn}`, { method: "DELETE" });
        alert("Libro eliminado ✅"); cargarLibrosDesdeSheets();
      }
    }

    function mostrarLibros() {
      const cont = document.getElementById("catalogo");
      cont.innerHTML = "";
      libros.forEach(libro => {
        cont.innerHTML += `
          <div>
            <strong>${libro.titulo}</strong> - ${libro.autor} (${libro.categoria}) - Stock: ${libro.cantidad}
            <button onclick="editarLibro('${libro.isbn}')">Editar</button>
            <button onclick="eliminarLibro('${libro.isbn}')">Eliminar</button>
          </div>`;
      });
    }

    function mostrarCatalogoEstudiante() {
      const cont = document.getElementById("catalogoEstudiante");
      cont.innerHTML = "";
      libros.forEach((libro, i) => {
        const div = document.createElement("div");
        div.innerHTML = `<strong>${libro.titulo}</strong> - ${libro.autor} (${libro.categoria})`;
        div.onclick = () => mostrarDetalleLibro(i);
        cont.appendChild(div);
      });
    }

    function mostrarDetalleLibro(i) {
      libroSeleccionado = i;
      const libro = libros[i];
      document.getElementById("tituloDetalle").textContent = libro.titulo;
      document.getElementById("autorDetalle").textContent = `Autor: ${libro.autor}`;
      document.getElementById("isbnDetalle").textContent = `ISBN: ${libro.isbn}`;
      document.getElementById("categoriaDetalle").textContent = `Categoría: ${libro.categoria}`;
      document.getElementById("cantidadDetalle").textContent = `Cantidad disponible: ${libro.cantidad}`;
      document.getElementById("detalleLibro").style.display = "block";
    }

    function alquilarLibro() {
      const dias = parseInt(document.getElementById("diasPrestamo").value);
      if (!dias || dias <= 0) { alert("Ingrese días válidos"); return; }
      const libro = libros[libroSeleccionado];
      if (libro.cantidad <= 0) { alert("No disponible"); return; }
      libro.cantidad--;
      const reg = { titulo: libro.titulo, fecha: new Date().toLocaleDateString(), dias };
      if (!historialPrestamos[usuarioActual.nombre]) historialPrestamos[usuarioActual.nombre] = [];
      historialPrestamos[usuarioActual.nombre].push(reg);
      guardarUsuarios();
      alert("Libro alquilado correctamente");
      document.getElementById("detalleLibro").style.display = "none";
      mostrarCatalogoEstudiante(); mostrarHistorial();
    }

    function mostrarHistorial() {
      const historial = historialPrestamos[usuarioActual.nombre] || [];
      const cont = document.getElementById("historialPrestamos");
      cont.innerHTML = "";
      historial.forEach(r => {
        const li = document.createElement("li");
        li.textContent = `${r.titulo} - Prestado el ${r.fecha} por ${r.dias} días`;
        cont.appendChild(li);
      });
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(HTML_PAGE)

if __name__ == "__main__":
    import uvicorn, os
    puerto = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=puerto)
