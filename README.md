# Industrial Vision Inspector

A computer vision project developed with **Python** and **OpenCV** that simulates an industrial quality inspection system. The application analyzes images from a production line, validates illumination conditions, detects edges, segments objects by color, analyzes connected components, and exports inspection metrics in JSON format.

---

## Features

- Image illumination auditing using the HSV Value channel.
- Automatic rejection of underexposed and overexposed images.
- Adaptive Canny edge detection based on image median.
- Gaussian filtering for noise reduction.
- HSV color segmentation.
- Morphological filtering (Opening and Closing).
- Connected components analysis.
- Automatic JSON report generation.
- Export of processed images.

---

## Project Structure

```
industrial-vision-inspector/
│
├── input_images/
│   ├── muestra_buena.jpg
│   ├── muestra_oscura.jpg
│   └── muestra_defectuosa.jpg
│
├── output_results/
│   ├── bordes_canny.png
│   └── mascara_limpia.png
│
├── vision_inspector.py
├── reporte_inspeccion.json
└── README.md
```

---

## Requirements

- Python 3.10+
- OpenCV
- NumPy

Install the required libraries:

```bash
pip install opencv-python numpy
```

---

## How to Run

Place your test images inside the `input_images/` folder.

Then execute:

```bash
python vision_inspector.py
```

The program will automatically:

1. Audit image illumination.
2. Apply Gaussian filtering.
3. Perform adaptive Canny edge detection.
4. Segment the target object using HSV color thresholds.
5. Apply morphological operations.
6. Detect connected components.
7. Generate processed images.
8. Export the inspection report as JSON.

---

## Output

Generated files include:

```
output_results/
├── bordes_canny.png
└── mascara_limpia.png

reporte_inspeccion.json
```

Example JSON output:

```json
{
  "archivo_procesado": "muestra_buena.jpg",
  "estado_auditoria": "APROBADO",
  "brillo_promedio_hsv": 128.45,
  "deteccion_bordes": {
    "umbral_inferior_canny": 86,
    "umbral_superior_canny": 170,
    "porcentaje_píxeles_borde": 4.12
  },
  "segmentacion_objetos": {
    "total_piezas_detectadas": 3,
    "porcentaje_area_ocupada": 18.35,
    "area_promedio_pieza_pixeles": 4520.67
  }
}
```

---

## Technologies

- Python
- OpenCV
- NumPy
- JSON

---

## Learning Objectives

This project demonstrates practical applications of:

- Image preprocessing
- Illumination analysis
- Adaptive edge detection
- Color segmentation in HSV
- Morphological image processing
- Connected component labeling
- Industrial computer vision
- Automated inspection pipelines

---

## License

This project was developed for educational purposes.