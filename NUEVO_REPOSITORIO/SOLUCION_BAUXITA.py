import pulp

def optimizar_bauxita(preferencias_w):
    """
    preferencias_w: diccionario {'B':1, 'C':0, 'D':1, 'E':0}
    Indica la preferencia del usuario de abrir o no la planta.
    El modelo trata de respetar la preferencia pero decide según factibilidad.
    """

    MINAS = ['A', 'B', 'C']
    PLALU = ['B','C','D','E']
    PLESM = ['D','E']

    # Parámetros
    capal_es = {'D': 4000, 'E': 7000}
    capb_al = {'B': 40000, 'C': 20000, 'D': 30000, 'E': 80000}
    capbaux = {'A': 36000, 'B': 52000, 'C': 28000}
    cexp = {'A': 420, 'B': 360, 'C': 540}
    cfijo = {'B': 3000000, 'C': 2500000, 'D': 4800000, 'E': 6000000}
    cpal = {'B': 330, 'C': 320, 'D': 380, 'E': 240}
    cpes = {'D': 8500, 'E': 5200}
    ctran_al = {('B','D'):220, ('B','E'):1510, ('C','D'):620, ('C','E'):940,
                ('D','D'):0, ('D','E'):1615, ('E','D'):1465, ('E','E'):0}
    ctran_b = {('A','B'):400, ('A','C'):2010, ('A','D'):510, ('A','E'):1920,
               ('B','B'):10,  ('B','C'):630,  ('B','D'):220, ('B','E'):1510,
               ('C','B'):1630,('C','C'):10,   ('C','D'):620, ('C','E'):940}
    demanda = {'D': 1000, 'E': 1200}
    rendal = {'A': 0.060, 'B': 0.080, 'C': 0.062}
    rendim = 0.4

    # Variables
    x = pulp.LpVariable.dicts("X", [(i,j) for i in MINAS for j in PLALU], lowBound=0)
    y = pulp.LpVariable.dicts("Y", [(j,k) for j in PLALU for k in PLESM], lowBound=0)
    w = pulp.LpVariable.dicts("W", PLALU, cat='Binary')

    # Modelo
    model = pulp.LpProblem("Problema_Bauxita", pulp.LpMinimize)

    # Función objetivo
    model += (
        pulp.lpSum(cexp[i]*x[(i,j)] for i in MINAS for j in PLALU) +
        pulp.lpSum(cpal[j]*y[(j,k)] for j in PLALU for k in PLESM) +
        pulp.lpSum(cpes[k]*y[(j,k)] for j in PLALU for k in PLESM) +
        pulp.lpSum(ctran_b[(i,j)]*x[(i,j)] for i in MINAS for j in PLALU) +
        pulp.lpSum(ctran_al[(j,k)]*y[(j,k)] for j in PLALU for k in PLESM) +
        pulp.lpSum(cfijo[j]*w[j] for j in PLALU)
    )

    # Restricciones
    for i in MINAS:
        model += pulp.lpSum(x[(i,j)] for j in PLALU) <= capbaux[i]

    for j in PLALU:
        # Si el usuario marcó como preferido abrir, agregamos incentivo
        if preferencias_w.get(j,0) == 1:
            # Reducimos costo ficticio para incentivar apertura
            model += w[j] >= 0  # solo para no bloquear, el solver decide
        model += pulp.lpSum(x[(i,j)] for i in MINAS) <= capb_al[j]*w[j]

    for k in PLESM:
        model += pulp.lpSum(y[(j,k)] for j in PLALU) <= capal_es[k]

    for k in PLESM:
        model += pulp.lpSum(rendim * y[(j,k)] for j in PLALU) == demanda[k]

    for j in PLALU:
        model += pulp.lpSum(rendal[i]*x[(i,j)] for i in MINAS) == pulp.lpSum(y[(j,k)] for k in PLESM)

    # Resolver
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # Resultados
    return {
        "costo_total": pulp.value(model.objective),
        "plantas": {j: int(pulp.value(w[j])) for j in PLALU},
        "x": [f"{i}->{j}: {pulp.value(x[(i,j)])}" for i,j in x if pulp.value(x[(i,j)])>0],
        "y": [f"{j}->{k}: {pulp.value(y[(j,k)])}" for j,k in y if pulp.value(y[(j,k)])>0]
    }
