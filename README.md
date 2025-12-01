# Sistema de Pedidos - Mesón

Aplicación Flask para gestionar pedidos en un mesón con pantalla de visualización en tiempo real.

## 🚀 Características

- **Página de Administración**: Interfaz para enviar pedidos con código y línea
- **Pantalla de Visualización**: Muestra los pedidos en tiempo real (ideal para TV/monitor)
- **Comunicación en Tiempo Real**: Usa Server-Sent Events (SSE) para actualizaciones instantáneas
- **Compatible con Vercel**: Optimizado para deployment serverless

## 📋 Requisitos Locales

- Python 3.7+
- Flask

## 🛠️ Instalación Local

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor:
```bash
python servidor.py
```

3. Abrir en el navegador:
   - **Admin**: http://localhost:5000/
   - **Display**: http://localhost:5000/display

## 🌐 Desplegar en Vercel

### Opción 1: Desde la Interfaz Web de Vercel

1. **Subir tu código a GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git push -u origin main
   ```

2. **Conectar con Vercel**:
   - Ve a [vercel.com](https://vercel.com)
   - Haz clic en "Add New Project"
   - Importa tu repositorio de GitHub
   - Vercel detectará automáticamente la configuración de `vercel.json`
   - Haz clic en "Deploy"

### Opción 2: Desde la CLI de Vercel

1. **Instalar Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Hacer login**:
   ```bash
   vercel login
   ```

3. **Desplegar**:
   ```bash
   vercel
   ```

4. **Para producción**:
   ```bash
   vercel --prod
   ```

## 📱 Uso

### Página de Administración (`/`)
1. Ingresa el código del pedido
2. Haz clic en el botón de la línea correspondiente (Línea 1, 2 o 3)
3. El pedido aparecerá automáticamente en todas las pantallas de visualización

### Pantalla de Visualización (`/display`)
- Muestra los pedidos en tiempo real
- Indicador de conexión en la esquina superior derecha
- Los pedidos más recientes aparecen arriba
- Ideal para mostrar en una TV o monitor

## 🔧 Configuración

El archivo `vercel.json` ya está configurado para Vercel. No necesitas modificarlo.

## 📝 Estructura del Proyecto

```
meson/
├── servidor.py          # Aplicación Flask principal
├── requirements.txt     # Dependencias Python
├── vercel.json         # Configuración de Vercel
└── README.md           # Este archivo
```

## 🐛 Solución de Problemas

### El servidor no inicia
- Verifica que Flask esté instalado: `pip install flask`
- Asegúrate de estar en el directorio correcto

### La pantalla de display no se actualiza
- Verifica que el indicador de conexión esté en verde
- Recarga la página
- Revisa la consola del navegador para errores

### Error en Vercel
- Asegúrate de que `vercel.json` esté en la raíz del proyecto
- Verifica que `requirements.txt` contenga solo `flask` y `gunicorn`
- Revisa los logs en el dashboard de Vercel

## 📄 Licencia

Este proyecto es de uso libre.

## ✨ Mejoras Futuras

- [ ] Autenticación para la página de admin
- [ ] Historial de pedidos
- [ ] Notificaciones sonoras
- [ ] Temas personalizables
- [ ] Soporte para múltiples idiomas
