import requests
from django.shortcuts import render

# URL de tu API en FastAPI (cámbiala si la despliegas en otro servidor)
API_PREDICT_URL = "http://127.0.0.1:8000/predict"


def _formatear_cop(valor: float) -> str:
    """Formatea un número en estilo colombiano: 250000000.5 -> 250.000.000,50."""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def index(request):
    """Renderiza el formulario del Tasador de Viviendas y consulta la API de FastAPI."""
    context = {
        # Datos del aprendiz / programa
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

        # Acepta tanto punto como coma decimal (ej: 85.5 o 45,2)
        m2_normalizado = m2_raw.replace(",", ".")

        try:
            m2_valor = float(m2_normalizado)
            if m2_valor <= 0:
                context["error"] = "El área de la vivienda debe ser mayor que 0 m²."
                return render(request, "tasador/index.html", context)
        except ValueError:
            context["error"] = "Ingresa un número válido para el área en m² (Ej: 85.5)."
            return render(request, "tasador/index.html", context)

        try:
            response = requests.post(
                API_PREDICT_URL,
                json={"m2": m2_valor},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                # Soporta 'precio_estimado' o nombres alternativos comunes
                raw_precio = (
                    data.get("precio_estimado")
                    if "precio_estimado" in data
                    else data.get("prediccion", data.get("precio"))
                )

                if raw_precio is None:
                    context["error"] = (
                        "La API respondió correctamente, pero no incluyó el campo de precio esperado."
                    )
                else:
                    precio = float(raw_precio)
                    context["precio_estimado"] = precio
                    context["precio_formateado"] = _formatear_cop(precio)
                    context["moneda"] = data.get("moneda", "COP")
            else:
                try:
                    detalle = response.json().get("detail", "Error al consultar el modelo.")
                except ValueError:
                    detalle = f"La API respondió con código de estado {response.status_code}."
                context["error"] = f"Error en la API: {detalle}"

        except requests.exceptions.ConnectionError:
            context["error"] = (
                f"No se pudo conectar con la API de predicción en {API_PREDICT_URL}. "
                "Verifica que FastAPI esté encendido."
            )
        except requests.exceptions.Timeout:
            context["error"] = "La solicitud a la API tardó demasiado tiempo en responder."
        except requests.exceptions.RequestException as exc:
            context["error"] = f"Error de red al consultar la API: {exc}"
        except (TypeError, ValueError) as exc:
            context["error"] = f"Error al interpretar la respuesta de la API: {exc}"

    return render(request, "tasador/index.html", context)