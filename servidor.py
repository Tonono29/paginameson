from flask import Flask, render_template_string, request
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

clientes = []

TV_PAGE = """<!DOCTYPE html>
<html>
<body style="font-family:sans-serif; background:black; color:white;">
<h1>Pedidos</h1>
<div id="lista"></div>

<script>
    const ws = new WebSocket("ws://" + location.host + "/ws");

    ws.onmessage = (event) => {
        const pedido = JSON.parse(event.data);
        const div = document.createElement("div");
        div.style.fontSize = "60px";
        div.style.marginBottom = "20px";
        div.style.padding = "20px";
        div.style.border = "3px solid white";
        div.textContent = pedido.codigo + "  —  " + pedido.linea;

        document.getElementById("lista").prepend(div);
    };
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

@app.route("/nuevo", methods=["POST"])
def nuevo():
    data = request.json
    mensaje = json.dumps(data)

    for c in clientes:
        try:
            c.send(mensaje)
        except:
            pass

    return "OK"

@sock.route('/ws')
def ws(ws):
    clientes.append(ws)
    while True:
        try:
            msg = ws.receive()
            if msg is None:
                break
        except:
            break
    clientes.remove(ws)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
