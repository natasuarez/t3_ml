import requests
from django.shortcuts import render

# URL de tu API en FastAPI (cámbiala si la despliegas en otro servidor)
API_PREDICT_URL = "http://127.0.0.1:8000/predict"


def index(request):
    """Renderiza el formulario del Tasador de Viviendas y consulta la API de FastAPI."""
    context = {
        # Datos solicitados del aprendiz / programa
        "nombre_aprendiz": "Natalia Peña Suarez",
        "numero_ficha": "3494620",
        "programa_formacion": "Analisis y Desarrollo de software (Adso)",
        # Valores dinámicos del formulario y respuesta de la API
        "m2_ingresado": "",
        "precio_estimado": None,
        "precio_formateado": None,
        "moneda": "COP",
        "error": None,
    }

    if request.method == "POST":
        m2_raw = request.POST.get("m2", "").strip()
        context["m2_ingresado"] = m2_raw

        # Validación básica del lado del servidor
        try:
            m2_valor = float(m2_raw)
            if m2_valor <= 0:
                context["error"] = "El área de la vivienda debe ser mayor que 0 m²."
                return render(request, "tasador/index.html", context)
        except ValueError:
            context["error"] = "Ingresa un número válido para el área en m² (Ej: 85.5)."
            return render(request, "tasador/index.html", context)

        # Consumo de la API de FastAPI mediante POST /predict
        try:
            response = requests.post(
                API_PREDICT_URL,
                json={"m2": m2_valor},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                precio = float(data.get("precio_estimado", 0))
                context["precio_estimado"] = precio
                # Formato legible en pesos colombianos (ej: $ 250.000.000,00)
                context["precio_formateado"] = f"{precio:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                context["moneda"] = data.get("moneda", "COP")
            else:
                try:
                    detalle = response.json().get("detail", "Error al consultar el modelo.")
                except Exception:
                    detalle = f"La API respondió con código de estado {response.status_code}."
                context["error"] = f"Error en la API: {detalle}"

        except requests.exceptions.ConnectionError:
            context["error"] = (
                "No se pudo conectar con la API de predicción en "
                f"{API_PREDICT_URL}. Verifica que FastAPI esté encendido."
            )
        except requests.exceptions.Timeout:
            context["error"] = "La solicitud a la API tardó demasiado tiempo en responder."
        except Exception as exc:
            context["error"] = f"Ocurrió un error inesperado: {exc}"

    return render(request, "tasador/index.html", context)