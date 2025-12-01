from flask import Flask, render_template_string, request, jsonify
import json
import time
from threading import Lock
from datetime import datetime, timedelta

app = Flask(__name__)

# Almacenamiento de mensajes en memoria
mensajes = []
mensajes_lock = Lock()

# Tiempo de vida de los mensajes (en segundos)
MENSAJE_TTL = 300  # 5 minutos

def limpiar_mensajes_antiguos():
    """Elimina mensajes más antiguos que MENSAJE_TTL"""
    now = time.time()
    with mensajes_lock:
        # Filtrar mensajes que no han expirado
        mensajes[:] = [m for m in mensajes if now - m['timestamp'] < MENSAJE_TTL]

TV_PAGE = """<!DOCTYPE html>
<html>
<body style="font-family:sans-serif; background:black; color:white;">
<h1>Pedidos</h1>
<div id="lista"></div>
<div id="status" style="position:fixed; top:10px; right:10px; font-size:14px; color:#888;"></div>

<script>
    let ultimoTimestamp = 0;
    let polling;
    
    function conectar() {
        document.getElementById("status").textContent = "● Conectado";
        document.getElementById("status").style.color = "#0f0";
        
        // Hacer polling cada 2 segundos
        polling = setInterval(async () => {
            try {
                const response = await fetch(`/stream?since=${ultimoTimestamp}`);
                
                if (!response.ok) {
                    throw new Error('Error en la conexión');
                }
                
                const data = await response.json();
                
                // Actualizar el timestamp
                if (data.timestamp) {
                    ultimoTimestamp = data.timestamp;
                }
                
                // Mostrar nuevos mensajes
                data.mensajes.forEach(pedido => {
                    const div = document.createElement("div");
                    div.style.fontSize = "60px";
                    div.style.marginBottom = "20px";
                    div.style.padding = "20px";
                    div.style.border = "3px solid white";
                    div.textContent = pedido.codigo + "  —  " + pedido.linea;
                    
                    document.getElementById("lista").prepend(div);
                });
                
                // Actualizar estado
                document.getElementById("status").textContent = "● Conectado";
                document.getElementById("status").style.color = "#0f0";
                
            } catch (error) {
                document.getElementById("status").textContent = "● Error";
                document.getElementById("status").style.color = "#f00";
                console.error('Error en polling:', error);
            }
        }, 2000);
    }
    
    // Limpiar al cerrar la página
    window.addEventListener('beforeunload', () => {
        if (polling) clearInterval(polling);
    });
    
    conectar();
</script>
</body>
</html>"""

ADMIN_PAGE = """<!DOCTYPE html>
<html>
<body style="font-family:sans-serif;">

<h1>Enviar pedido</h1>
<input id="codigo" placeholder="Código del pedido" style="font-size:20px; padding:10px;" />

<br><br>
<button onclick="enviar('Línea 1')" style="font-size:20px;">Línea 1</button>
<button onclick="enviar('Línea 2')" style="font-size:20px;">Línea 2</button>
<button onclick="enviar('Línea 3')" style="font-size:20px;">Línea 3</button>

<script>
function enviar(linea) {
    const codigo = document.getElementById("codigo").value;

    fetch("/nuevo", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({codigo, linea})
    });

    document.getElementById("codigo").value = "";
}
</script>
</body>
</html>"""

@app.route("/")
def admin():
    return render_template_string(ADMIN_PAGE)

@app.route("/display")
def tv():
    return render_template_string(TV_PAGE)

@app.route("/stream")
def stream():
    """Endpoint de polling que devuelve mensajes nuevos desde el último timestamp"""
    # Limpiar mensajes antiguos
    limpiar_mensajes_antiguos()
    
    # Obtener el timestamp desde el cual el cliente quiere mensajes
    since = float(request.args.get('since', 0))
    
    # Filtrar mensajes nuevos
    with mensajes_lock:
        nuevos_mensajes = [
            m['data'] for m in mensajes 
            if m['timestamp'] > since
        ]
    
    # Devolver mensajes y timestamp actual
    return jsonify({
        'mensajes': nuevos_mensajes,
        'timestamp': time.time()
    })

@app.route("/nuevo", methods=["POST"])
def nuevo():
    data = request.json
    
    # Agregar mensaje con timestamp
    with mensajes_lock:
        mensajes.append({
            'data': data,
            'timestamp': time.time()
        })
    
    # Limpiar mensajes antiguos
    limpiar_mensajes_antiguos()
    
    return "OK"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
