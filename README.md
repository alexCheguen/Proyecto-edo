# Calculadora de Ecuaciones Diferenciales Ordinarias (EDO)

**Proyecto de Ecuaciones Diferenciales - Primer Orden**

---

## Descripción del Proyecto

Calculadora web desarrollada con **Vue.js** (frontend) y **Python/FastAPI** (backend) que resuelve ecuaciones diferenciales ordinarias de primer orden mediante métodos analíticos.

### Tipos de EDO Soportadas

1. **Ecuaciones Separables**: `dy/dx = g(x)h(y)`
2. **Ecuaciones Exactas**: `M(x,y)dx + N(x,y)dy = 0`
3. **Ecuaciones Lineales**: `dy/dx + P(x)y = Q(x)`
4. **Ecuaciones de Bernoulli**: `dy/dx + P(x)y = Q(x)y^n`

---

## Instalación y Ejecución

### Requisitos Previos

- Python 3.8 o superior
- Navegador web moderno
- pip (gestor de paquetes de Python)

### Paso 1: Configurar el Backend

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
python main.py
```

El backend estará disponible en: `http://localhost:8000`

### Paso 2: Abrir el Frontend

Simplemente abra el archivo `index.html` en su navegador web, o puede usar un servidor local:

```bash
# Con Python
python -m http.server 3000

# Luego abrir: http://localhost:3000
```

---

## Fundamento Matemático

### 1. Ecuaciones Separables

**Forma general**: `dy/dx = g(x)h(y)`

**Método**:

1. Separar variables: `dy/h(y) = g(x)dx`
2. Integrar ambos lados: `∫dy/h(y) = ∫g(x)dx + C`

**Ejemplo**:

- Ecuación: `dy/dx = xy`
- Separación: `dy/y = x dx`
- Integración: `ln|y| = x²/2 + C`
- Solución: `y = C₁e^(x²/2)`

### 2. Ecuaciones Exactas

**Forma general**: `M(x,y)dx + N(x,y)dy = 0`

**Condición de exactitud**: `∂M/∂y = ∂N/∂x`

**Método**:

1. Verificar condición de exactitud
2. Encontrar función potencial `F(x,y)` tal que:
   - `∂F/∂x = M(x,y)`
   - `∂F/∂y = N(x,y)`
3. Solución implícita: `F(x,y) = C`

**Ejemplo**:

- Ecuación: `(2xy)dx + (x²)dy = 0`
- M = 2xy, N = x²
- ∂M/∂y = 2x, ∂N/∂x = 2x ✓ (es exacta)
- F(x,y) = x²y
- Solución: `x²y = C`

### 3. Ecuaciones Lineales

**Forma general**: `dy/dx + P(x)y = Q(x)`

**Método del Factor Integrante**:

1. Factor integrante: `μ(x) = e^(∫P(x)dx)`
2. Multiplicar toda la ecuación por μ(x)
3. Reconocer: `d/dx[μ(x)y] = μ(x)Q(x)`
4. Integrar: `μ(x)y = ∫μ(x)Q(x)dx + C`
5. Despejar: `y = [∫μ(x)Q(x)dx + C]/μ(x)`

**Ejemplo**:

- Ecuación: `dy/dx + (2x)y = x²`
- P(x) = 2x, Q(x) = x²
- μ(x) = e^(∫2x dx) = e^(x²)
- Solución: `y = [∫x²e^(x²)dx + C]/e^(x²)`

### 4. Ecuaciones de Bernoulli

**Forma general**: `dy/dx + P(x)y = Q(x)y^n`

**Método de Sustitución**:

1. Sustitución: `v = y^(1-n)`
2. Derivar: `dv/dx = (1-n)y^(-n)dy/dx`
3. Dividir ecuación original entre `y^n`
4. Sustituir para obtener ecuación lineal en v:
   `dv/dx + (1-n)P(x)v = (1-n)Q(x)`
5. Resolver como ecuación lineal
6. Regresar a y: `y = v^(1/(1-n))`

**Ejemplo**:

- Ecuación: `dy/dx + (1/x)y = xy²` (n=2)
- Sustitución: `v = y^(-1)`
- Ecuación lineal: `dv/dx - (1/x)v = -x`
- Resolver y regresar a y

---

## Guía de Uso

### Ecuaciones Separables

**Formato de entrada**: `expresión en términos de x e y`

Ejemplos:

- `x*y` → dy/dx = xy
- `x**2/(1+y**2)` → dy/dx = x²/(1+y²)
- `exp(x)*y` → dy/dx = e^x · y

### Ecuaciones Exactas

**Formato de entrada**: `M(x,y)|N(x,y)`

Ejemplos:

- `2*x*y|x**2` → (2xy)dx + (x²)dy = 0
- `2*x + y|x` → (2x+y)dx + (x)dy = 0

### Ecuaciones Lineales

**Formato de entrada**: `P(x)|Q(x)`

Ejemplos:

- `2*x|x**2` → dy/dx + 2xy = x²
- `1/x|x` → dy/dx + (1/x)y = x
- `1|exp(x)` → dy/dx + y = e^x

### Ecuaciones de Bernoulli

**Formato de entrada**: `P(x)|Q(x)|n`

Ejemplos:

- `1/x|x|2` → dy/dx + (1/x)y = xy²
- `1|1|3` → dy/dx + y = y³

### Operadores Matemáticos Disponibles

- Suma: `+`
- Resta: `-`
- Multiplicación: `*`
- División: `/`
- Potencia: `**` (ejemplo: `x**2` para x²)
- Exponencial: `exp(x)` para e^x
- Logaritmo natural: `log(x)` para ln(x)
- Seno: `sin(x)`
- Coseno: `cos(x)`
- Tangente: `tan(x)`

---

## Estructura del Proyecto

```
proyecto-edo/
│
├── main.py                 # Backend FastAPI
├── index.html             # Frontend Vue.js
├── requirements.txt       # Dependencias Python
└── README.md             # Documentación
```

---

## Ejemplos de Uso

### Ejemplo 1: Ecuación Separable

**Input**: `x*y`  
**Tipo**: Separable  
**Salida**: `Eq(log(y(x)), C1 + x**2/2)`  
**Interpretación**: `ln(y) = C₁ + x²/2` → `y = Ce^(x²/2)`

### Ejemplo 2: Ecuación Exacta

**Input**: `2*x*y|x**2`  
**Tipo**: Exacta  
**Salida**: `Eq(x**2*y, C1)`  
**Interpretación**: `x²y = C`

### Ejemplo 3: Ecuación Lineal

**Input**: `1|exp(x)`  
**Tipo**: Lineal  
**Salida**: Solución con factor integrante

### Ejemplo 4: Ecuación de Bernoulli

**Input**: `1/x|x|2`  
**Tipo**: Bernoulli  
**Salida**: Solución mediante sustitución v = y^(-1)

---

## Validación y Pruebas

### Casos de Prueba Implementados

1. **Separables**:

   - ✅ `xy` → Separable simple
   - ✅ `x**2/(1+y**2)` → Con funciones complejas

2. **Exactas**:

   - ✅ `2*x*y|x**2` → Exacta directa
   - ✅ Verificación de condición ∂M/∂y = ∂N/∂x

3. **Lineales**:

   - ✅ `2*x|x**2` → Con factor integrante
   - ✅ `1/x|x` → Con P(x) racional

4. **Bernoulli**:
   - ✅ `1/x|x|2` → n=2
   - ✅ Verificación de sustitución correcta

---

## Aprendizajes y Conclusiones

### Aspectos Técnicos

- Implementación de algoritmos simbólicos usando SymPy
- Integración de frontend-backend mediante API REST
- Manejo de expresiones matemáticas en formato texto

### Aspectos Matemáticos

- Comprensión profunda de métodos de solución de EDO
- Identificación automática de tipos de ecuaciones
- Validación de condiciones necesarias (exactitud, linealidad)

### Desafíos Enfrentados

1. Parsing correcto de expresiones matemáticas
2. Manejo de casos especiales y excepciones
3. Presentación clara de pasos de solución

### Mejoras Futuras

- Graficación de soluciones
- Más tipos de EDO (Ricatti, Clairaut)
- Resolución de sistemas de EDO
- Métodos numéricos (Euler, Runge-Kutta)

---

## Licencia y Créditos

**Autor**: [Tu Nombre]  
**Curso**: Ecuaciones Diferenciales  
**Institución**: [Tu Universidad]  
**Fecha**: Noviembre 2025

**Tecnologías Utilizadas**:

- Python 3.x
- FastAPI
- SymPy
- Vue.js 3
- Axios

---

## Soporte

Para preguntas o problemas:

- Revisar la documentación de SymPy: https://docs.sympy.org
- Documentación de FastAPI: https://fastapi.tiangolo.com

---

## Checklist de Entregables

- [x] Código fuente completo y documentado
- [x] Backend funcional con 4 tipos de EDO
- [x] Frontend interactivo con Vue.js
- [x] Ejemplos de uso para cada tipo
- [x] Documentación técnica (README)
- [x] Validación matemática de resultados
- [ ] Presentación oral preparada
- [ ] Reporte técnico en PDF

---

**¡Proyecto completado exitosamente! 🎉**
