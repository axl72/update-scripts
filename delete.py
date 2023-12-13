from datetime import datetime, timedelta

# Definir el rango de fechas
inicio_rango = datetime(2023, 12, 26)
fin_rango = datetime(2025, 1, 15)

# Encontrar el primer lunes del año
primer_lunes = datetime(inicio_rango.year, 1, 1)
while primer_lunes.weekday() != 0:  # 0 representa lunes en Python
    primer_lunes += timedelta(days=1)

# Determinar el número de semanas transcurridas desde el primer lunes del año hasta la fecha de inicio
numero_semanas = ((inicio_rango - primer_lunes).days // 7) + 1

print(f"La semana comercial correspondiente al rango de fechas {inicio_rango.strftime('%Y-%m-%d')} al {fin_rango.strftime('%Y-%m-%d')} es la semana {numero_semanas}.")
