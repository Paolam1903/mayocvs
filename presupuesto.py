import pandas as pd

# =====================
# REGLA DE DISTRIBUCIÓN
# =====================
def calcular_distribucion(n_asesores, cvs, nombre=None, rol=None):

    cvs = str(cvs).upper()
    nombre = str(nombre).upper() if nombre else ""

    # ==================================================
    # 🔴 REGLA ESPECIAL SABANETA
    # ==================================================
    # Metas puntos:
    # Líder Sandra = 845
    # Andrea Arenas = 1267.5
    # Maria Fernanda = 487.5
    #
    # La suma total = 2600
    #
    # Se convierte a porcentaje para productos y puntos
    # ==================================================

    if cvs == "SABANETA":

        # 👔 LÍDER
        if rol == "LIDER":
            return 845 / 2600

        # 👩 Andrea
        elif "ANDREA" in nombre:
            return 1267.5 / 2600

        # 👩 Maria Fernanda
        elif "FERNANDA" in nombre or "MARIA FERNANDA" in nombre:
            return 487.5 / 2600
        


    # ==================================================
    # 🔴 REGLA ESPECIAL COPACABANA
    # ==================================================
    if cvs == "COPACABANA":

        # TOTAL META = 3000 aprox
        # Vanessa = 1031
        # Alexa = 1547
        # Bibiana = 421.8

        # 👩 Vanessa
        if "VANESSA" in nombre:
            return 1031 / 3000

        # 👩 Alexa
        elif "ALEXA" in nombre:
            return 1547 / 3000

        # 👩 Bibiana
        elif "BIBIANA" in nombre:
            return 421.8 / 3000


    # ==================================================
    # 🔴 REGLA ESPECIAL ITAGUI
    # ==================================================
    if cvs == "ITAGUI":

        # TOTAL META = 2500
        # Marcela = 797
        # Dailyn = 1195
        # Jhon = 508

        # 👩 Marcela
        if "MARCELA" in nombre:
            return 797 / 2500

        # 👩 Dailyn
        elif "DAILYN" in nombre:
            return 1195 / 2500

        # 👨 Jhon
        elif "JHON" in nombre:
            return 508 / 2500

    # ==================================================
    # 🔴 REGLA ESPECIAL FRONTINO
    # ==================================================
    if cvs == "FRONTINO":
        return 0.50

    # ==================================================
    # 🔴 REGLAS NORMALES
    # ==================================================

    # Si no hay asesores
    if n_asesores == 0:
        return 1.0

    if rol == "LIDER":

        if n_asesores == 1:
            return 0.40
        elif n_asesores == 2:
            return 0.25
        elif n_asesores >= 3:
            return 0.20

    else:

        if n_asesores == 1:
            return 0.60
        elif n_asesores == 2:
            return 0.375
        elif n_asesores >= 3:
            return 0.266

    return 1.0


# =================================================
# META GENERAL + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_meta_general_por_cvs(df):
    resultados = []

    for sucursal, grupo in df.groupby("Sucursal"):
        meta_total = grupo["Meta_General"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Estructura": f"1 Líder + {n_asesores} Asesor(es)",

            "Meta CVS": meta_total,

            "Meta Líder": meta_total * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_total * pct_lider)) * 100, 2
            ) if meta_total * pct_lider > 0 else 0,

            "Meta Asesores": meta_total * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_total * pct_asesores)) * 100, 2
            ) if meta_total * pct_asesores > 0 else 0,
        })

    return pd.DataFrame(resultados)


# =================================================
# KPI POR PRODUCTO + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_kpi_producto_por_cvs(df):
    resultados = []

    for (sucursal, producto), grupo in df.groupby(["Sucursal", "Producto"]):
        meta_producto = grupo["Meta_Producto"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Producto": producto,

            "Meta Producto": meta_producto,

            "Meta Líder": meta_producto * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_producto * pct_lider)) * 100, 2
            ) if meta_producto * pct_lider >= 0 else 0,

            "Meta Asesores": meta_producto * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_producto * pct_asesores)) * 100, 2
            ) if meta_producto * pct_asesores >= 0 else 0,
        })

    return pd.DataFrame(resultados)
