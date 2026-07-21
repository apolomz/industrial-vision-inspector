import cv2
import numpy as np
import os
import json


# ===============================
# ETAPA 1 - Auditoría de iluminación
# ===============================

def auditar_iluminacion(imagen):

    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    brillo = np.mean(hsv[:, :, 2])

    if brillo < 40 or brillo > 220:
        return False, brillo

    return True, brillo


# ===============================
# ETAPA 2 - Canny Adaptativo
# ===============================

def canny_adaptativo(imagen_gris):

    blur = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

    mediana = np.median(blur)

    inferior = int(max(0, (1 - 0.33) * mediana))
    superior = int(min(255, (1 + 0.33) * mediana))

    bordes = cv2.Canny(blur, inferior, superior)

    return bordes, inferior, superior


# ===============================
# ETAPA 3 - Segmentación HSV
# ===============================

def segmentar_objeto(imagen):

    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # ===== EJEMPLO PARA OBJETOS VERDES =====
    verde_bajo = np.array([35, 40, 40])
    verde_alto = np.array([90, 255, 255])

    mascara = cv2.inRange(hsv, verde_bajo, verde_alto)

    kernel_open = np.ones((5, 5), np.uint8)
    kernel_close = np.ones((7, 7), np.uint8)

    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_OPEN,
        kernel_open
    )

    mascara = cv2.morphologyEx(
        mascara,
        cv2.MORPH_CLOSE,
        kernel_close
    )

    return mascara


# ===============================
# ETAPA 4 - Componentes conectados
# ===============================

def analizar_componentes(mascara):

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mascara,
        connectivity=8
    )

    areas = []

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]

        areas.append(int(area))

    total_objetos = len(areas)

    area_promedio = 0

    if total_objetos > 0:
        area_promedio = float(np.mean(areas))

    return total_objetos, areas, area_promedio


# ===============================
# Función principal
# ===============================

def inspeccionar_imagen(ruta):

    output_dir = "output_results"
    os.makedirs(output_dir, exist_ok=True)

    imagen = cv2.imread(ruta)

    if imagen is None:
        print("No se pudo cargar la imagen.")
        return

    nombre = os.path.basename(ruta)

    aprobado, brillo = auditar_iluminacion(imagen)

    if not aprobado:

        reporte = {
            "archivo_procesado": nombre,
            "estado_auditoria": "REJECTED_ILLUMINATION",
            "brillo_promedio_hsv": round(brillo, 2)
        }

        with open("reporte_inspeccion.json", "w", encoding="utf-8") as f:
            json.dump(reporte, f, indent=4, ensure_ascii=False)

        print("Imagen rechazada por iluminación.")
        return

    # ==========================
    # Canny
    # ==========================

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    bordes, inf, sup = canny_adaptativo(gris)

    cv2.imwrite(
        os.path.join(output_dir, "bordes_canny.png"),
        bordes
    )

    porcentaje_bordes = (
        np.count_nonzero(bordes)
        / bordes.size
        * 100
    )

    # ==========================
    # Segmentación
    # ==========================

    mascara = segmentar_objeto(imagen)

    cv2.imwrite(
        os.path.join(output_dir, "mascara_limpia.png"),
        mascara
    )

    porcentaje_area = (
        np.count_nonzero(mascara)
        / mascara.size
        * 100
    )

    # ==========================
    # Componentes
    # ==========================

    total_objetos, areas, area_promedio = analizar_componentes(
        mascara
    )

    reporte = {

        "archivo_procesado": nombre,

        "estado_auditoria": "APROBADO",

        "brillo_promedio_hsv": round(brillo, 2),

        "deteccion_bordes": {

            "umbral_inferior_canny": inf,
            "umbral_superior_canny": sup,
            "porcentaje_píxeles_borde": round(
                porcentaje_bordes,
                2
            )
        },

        "segmentacion_objetos": {

            "total_piezas_detectadas": total_objetos,

            "areas_individuales_pixeles": areas,

            "porcentaje_area_ocupada": round(
                porcentaje_area,
                2
            ),

            "area_promedio_pieza_pixeles": round(
                area_promedio,
                2
            )
        }
    }

    with open(
        "reporte_inspeccion.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            reporte,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Inspección finalizada correctamente.")


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":

    ruta = "input_images/muestra_buena.png"

    inspeccionar_imagen(ruta)