"""Report generation for inspection results."""
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import List, Optional


def utc_timestamp() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class InspectionReport:
    """Structured result of running the pipeline on a single image.

    Serializes to the same nested JSON shape used by the original script
    (``deteccion_bordes`` / ``segmentacion_objetos``), so existing
    downstream consumers of the report keep working.
    """

    archivo_procesado: str
    estado_auditoria: str
    brillo_promedio_hsv: float
    timestamp_utc: str
    umbral_inferior_canny: Optional[int] = None
    umbral_superior_canny: Optional[int] = None
    porcentaje_pixeles_borde: Optional[float] = None
    total_piezas_detectadas: Optional[int] = None
    areas_individuales_pixeles: Optional[List[int]] = None
    porcentaje_area_ocupada: Optional[float] = None
    area_promedio_pieza_pixeles: Optional[float] = None

    def to_dict(self) -> dict:
        data = asdict(self)

        nested = {
            "archivo_procesado": data["archivo_procesado"],
            "estado_auditoria": data["estado_auditoria"],
            "timestamp_utc": data["timestamp_utc"],
            "brillo_promedio_hsv": data["brillo_promedio_hsv"],
        }

        if data["umbral_inferior_canny"] is not None:
            nested["deteccion_bordes"] = {
                "umbral_inferior_canny": data["umbral_inferior_canny"],
                "umbral_superior_canny": data["umbral_superior_canny"],
                "porcentaje_píxeles_borde": data["porcentaje_pixeles_borde"],
            }

        if data["total_piezas_detectadas"] is not None:
            nested["segmentacion_objetos"] = {
                "total_piezas_detectadas": data["total_piezas_detectadas"],
                "areas_individuales_pixeles": data["areas_individuales_pixeles"],
                "porcentaje_area_ocupada": data["porcentaje_area_ocupada"],
                "area_promedio_pieza_pixeles": data["area_promedio_pieza_pixeles"],
            }

        return nested

    def save(self, path: str) -> None:
        """Write this report to disk as pretty-printed UTF-8 JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
