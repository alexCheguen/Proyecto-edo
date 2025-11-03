# Guía de Instalación y Ejecución - Proyecto EDO

## 📋 Pasos de Instalación

### 1. Verificar Python

```bash
python --version
# Debe ser Python 3.8 o superior
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el proyecto

#### Opción A: Script automático (Recomendado)

```bash
python start.py
```

#### Opción B: Manual

```bash
# Terminal 1 - Backend
python main.py

# Terminal 2 - Frontend (en otra ventana)
python -m http.server 3000

# Luego abrir: http://localhost:3000
```

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error: Puerto ocupado

- Cambiar puerto en main.py línea 314: `port=8001`
- O cerrar otros procesos que usen el puerto 8000

### Error: CORS

- Verificar que el backend esté ejecutándose en localhost:8000
- El frontend debe acceder desde localhost:3000

## 🧪 Probar Funcionalidad

### Ecuaciones de prueba:

**Separables:**

- `x*y`
- `x**2/(1+y**2)`

**Exactas:**

- `2*x*y|x**2`
- `2*x + y|x`

**Lineales:**

- `2*x|x**2`
- `1/x|x`

**Bernoulli:**

- `1/x|x|2`
- `1|1|3`

## 📁 Estructura del Proyecto

```
proyecto-edo/
├── main.py              # Backend FastAPI
├── index.html           # Frontend Vue.js
├── requirements.txt     # Dependencias
├── start.py            # Script de inicio
├── test_functions.py   # Tests de funciones
└── README.md           # Documentación
```

## 🌐 URLs del Proyecto

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
