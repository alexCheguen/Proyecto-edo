"""
Calculadora de Ecuaciones Diferenciales Ordinarias (EDO) de Primer Orden
Backend API con FastAPI

Resuelve EDO de tipo:
- Separables
- Exactas
- Lineales
- Bernoulli
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sympy import symbols, Function, Eq, dsolve, sympify, diff, integrate, simplify, exp, log
from sympy.parsing.sympy_parser import parse_expr
import re

app = FastAPI(title="EDO Solver API")

# Configurar CORS para permitir peticiones desde Vue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EDORequest(BaseModel):
    equation: str
    tipo: str
    initial_x: Optional[float] = None
    initial_y: Optional[float] = None

class EDOResponse(BaseModel):
    success: bool
    solution: str
    solution_latex: str = ""
    particular_solution: str = ""
    steps: list = []
    plot_data: dict = None
    error: str = ""

x, y, C1, C2 = symbols('x y C1 C2')
f = Function('f')

def classify_and_solve_separable(equation_str):
    """
    Resuelve EDO Separables: dy/dx = g(x)h(y)
    Método: Separar variables e integrar ambos lados
    """
    steps = []
    try:
        # Parsear ecuación en formato dy/dx = f(x,y)
        eq_parts = equation_str.replace("dy/dx", "").replace("=", "").strip()
        expr = parse_expr(eq_parts, local_dict={'x': x, 'y': y})
        
        steps.append("1. Ecuación original: dy/dx = " + str(expr))
        
        # Crear ecuación diferencial
        y_func = Function('y')(x)
        ode = Eq(y_func.diff(x), expr.subs(y, y_func))
        
        steps.append("2. Ecuación en formato simbólico: " + str(ode))
        steps.append("3. Método: Separación de variables")
        steps.append("4. Separar: dy/h(y) = g(x)dx")
        
        # Resolver
        solution = dsolve(ode, y_func)
        steps.append("5. Integrar ambos lados")
        steps.append("6. Solución general: " + str(solution))
        
        return solution, steps
    except Exception as e:
        raise Exception(f"Error resolviendo separable: {str(e)}")

def classify_and_solve_exact(M_str, N_str):
    """
    Resuelve EDO Exactas: M(x,y)dx + N(x,y)dy = 0
    Condición: ∂M/∂y = ∂N/∂x
    """
    steps = []
    try:
        M = parse_expr(M_str, local_dict={'x': x, 'y': y})
        N = parse_expr(N_str, local_dict={'x': x, 'y': y})
        
        steps.append("1. Ecuación: M(x,y)dx + N(x,y)dy = 0")
        steps.append(f"   M(x,y) = {M}")
        steps.append(f"   N(x,y) = {N}")
        
        # Verificar exactitud
        dM_dy = diff(M, y)
        dN_dx = diff(N, x)
        
        steps.append(f"2. Verificar exactitud: ∂M/∂y = {dM_dy}")
        steps.append(f"   ∂N/∂x = {dN_dx}")
        
        if simplify(dM_dy - dN_dx) != 0:
            steps.append("   ⚠ La ecuación NO es exacta")
            raise Exception("La ecuación no es exacta")
        
        steps.append("   ✓ La ecuación es exacta")
        
        # Encontrar función potencial F(x,y)
        steps.append("3. Integrar M respecto a x:")
        F = integrate(M, x)
        steps.append(f"   F(x,y) = {F} + g(y)")
        
        # Derivar F respecto a y y comparar con N
        dF_dy = diff(F, y)
        g_prime = simplify(N - dF_dy)
        
        steps.append("4. Derivar F respecto a y e igualar a N:")
        steps.append(f"   ∂F/∂y = {dF_dy}")
        steps.append(f"   g'(y) = N - ∂F/∂y = {g_prime}")
        
        g = integrate(g_prime, y)
        steps.append(f"5. Integrar g'(y): g(y) = {g}")
        
        F_complete = F + g
        solution = Eq(F_complete, C1)
        
        steps.append(f"6. Solución implícita: {solution}")
        
        return solution, steps
    except Exception as e:
        raise Exception(f"Error resolviendo exacta: {str(e)}")

def classify_and_solve_linear(P_str, Q_str):
    """
    Resuelve EDO Lineales: dy/dx + P(x)y = Q(x)
    Método: Factor integrante μ(x) = e^(∫P(x)dx)
    """
    steps = []
    try:
        P = parse_expr(P_str, local_dict={'x': x, 'y': y})
        Q = parse_expr(Q_str, local_dict={'x': x, 'y': y})
        
        steps.append("1. Ecuación lineal: dy/dx + P(x)y = Q(x)")
        steps.append(f"   P(x) = {P}")
        steps.append(f"   Q(x) = {Q}")
        
        # Factor integrante
        steps.append("2. Calcular factor integrante: μ(x) = e^(∫P(x)dx)")
        P_integral = integrate(P, x)
        mu = exp(P_integral)
        steps.append(f"   ∫P(x)dx = {P_integral}")
        steps.append(f"   μ(x) = {mu}")
        
        # Multiplicar por factor integrante
        steps.append("3. Multiplicar toda la ecuación por μ(x):")
        steps.append("   d/dx[μ(x)y] = μ(x)Q(x)")
        
        # Integrar
        steps.append("4. Integrar ambos lados:")
        right_side = simplify(mu * Q)
        integral_result = integrate(right_side, x)
        steps.append(f"   ∫μ(x)Q(x)dx = {integral_result}")
        
        # Solución
        solution_expr = (integral_result + C1) / mu
        solution = Eq(y, simplify(solution_expr))
        
        steps.append(f"5. Solución general: y = [∫μ(x)Q(x)dx + C₁]/μ(x)")
        steps.append(f"   {solution}")
        
        return solution, steps
    except Exception as e:
        raise Exception(f"Error resolviendo lineal: {str(e)}")

def classify_and_solve_bernoulli(P_str, Q_str, n_val):
    """
    Resuelve EDO de Bernoulli: dy/dx + P(x)y = Q(x)y^n
    Método: Sustitución v = y^(1-n) para convertir a lineal
    """
    steps = []
    try:
        P = parse_expr(P_str, local_dict={'x': x, 'y': y})
        Q = parse_expr(Q_str, local_dict={'x': x, 'y': y})
        n = float(n_val)
        
        steps.append("1. Ecuación de Bernoulli: dy/dx + P(x)y = Q(x)y^n")
        steps.append(f"   P(x) = {P}")
        steps.append(f"   Q(x) = {Q}")
        steps.append(f"   n = {n}")
        
        if n == 0 or n == 1:
            steps.append("   ⚠ Para n=0 o n=1, es una ecuación lineal estándar")
        
        # Sustitución
        steps.append(f"2. Sustitución: v = y^(1-n) = y^{1-n}")
        steps.append(f"3. Derivar: dv/dx = (1-n)y^(-n)dy/dx = {1-n}y^{-n}dy/dx")
        
        # Dividir entre y^n
        steps.append(f"4. Dividir la ecuación original entre y^n:")
        steps.append(f"   y^(-n)dy/dx + P(x)y^(1-n) = Q(x)")
        
        # Sustituir
        steps.append(f"5. Sustituir v y dv/dx:")
        steps.append(f"   dv/dx + (1-n)P(x)v = (1-n)Q(x)")
        
        # Nueva ecuación lineal
        P_new = (1-n) * P
        Q_new = (1-n) * Q
        
        steps.append("6. Esta es una ecuación lineal en v(x)")
        steps.append(f"   dv/dx + {P_new}v = {Q_new}")
        
        # Resolver como lineal
        P_integral = integrate(P_new, x)
        mu = exp(P_integral)
        steps.append(f"7. Factor integrante: μ(x) = e^(∫{P_new}dx) = {mu}")
        
        right_side = simplify(mu * Q_new)
        integral_result = integrate(right_side, x)
        
        v_solution = (integral_result + C1) / mu
        steps.append(f"8. Solución para v: v = {simplify(v_solution)}")
        
        # Volver a y
        y_solution = v_solution ** (1/(1-n))
        solution = Eq(y, simplify(y_solution))
        
        steps.append(f"9. Como v = y^(1-n), entonces y = v^(1/(1-n))")
        steps.append(f"   {solution}")
        
        return solution, steps
    except Exception as e:
        raise Exception(f"Error resolviendo Bernoulli: {str(e)}")

@app.post("/solve", response_model=EDOResponse)
async def solve_edo(request: EDORequest):
    """
    Endpoint principal para resolver EDO
    """
    try:
        solution = None
        steps = []
        
        if request.tipo == "separable":
            solution, steps = classify_and_solve_separable(request.equation)
            
        elif request.tipo == "exacta":
            # Formato esperado: "M(x,y)|N(x,y)"
            parts = request.equation.split("|")
            if len(parts) != 2:
                raise HTTPException(400, "Formato incorrecto. Use: M(x,y)|N(x,y)")
            solution, steps = classify_and_solve_exact(parts[0].strip(), parts[1].strip())
            
        elif request.tipo == "lineal":
            # Formato esperado: "P(x)|Q(x)"
            parts = request.equation.split("|")
            if len(parts) != 2:
                raise HTTPException(400, "Formato incorrecto. Use: P(x)|Q(x)")
            solution, steps = classify_and_solve_linear(parts[0].strip(), parts[1].strip())
            
        elif request.tipo == "bernoulli":
            # Formato esperado: "P(x)|Q(x)|n"
            parts = request.equation.split("|")
            if len(parts) != 3:
                raise HTTPException(400, "Formato incorrecto. Use: P(x)|Q(x)|n")
            solution, steps = classify_and_solve_bernoulli(
                parts[0].strip(), 
                parts[1].strip(), 
                parts[2].strip()
            )
        else:
            raise HTTPException(400, f"Tipo de ecuación no soportado: {request.tipo}")
        
        # Convertir solución a string
        solution_str = str(solution)
        
        # Solución particular si hay condiciones iniciales
        particular = ""
        if request.initial_x is not None and request.initial_y is not None:
            try:
                # Aquí se implementaría el cálculo de la solución particular
                particular = f"Condiciones iniciales: y({request.initial_x}) = {request.initial_y}"
            except:
                pass
        
        return EDOResponse(
            success=True,
            solution=solution_str,
            solution_latex=solution_str,
            particular_solution=particular,
            steps=steps
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        return EDOResponse(
            success=False,
            solution="",
            error=str(e)
        )

@app.get("/")
async def root():
    return {
        "message": "API Calculadora EDO",
        "version": "1.0",
        "tipos_soportados": ["separable", "exacta", "lineal", "bernoulli"]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)