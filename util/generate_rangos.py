import datetime

# Define el año que deseas analizar como parámetro
año = 2022  # Cambia esto al año que desees

# Crea una fecha inicial para el 1 de enero del año especificado
fecha = datetime.date(año, 1, 1)

lunes = []
viernes = []
# Itera a lo largo de todo el año
while fecha.year == año:
    # Verifica si el día de la semana es lunes (0) o domingo (6)
    if fecha.weekday() == 0:
        lunes.append(fecha.strftime("%d/%m/%Y"))
        viernes.append((fecha + datetime.timedelta(days=6)).strftime("%d/%m/%Y"))

    # Avanza un día
    fecha += datetime.timedelta(days=1)

print("Lunes", len(lunes))
# print(*lunes, sep='\n')
print("Viernes", len(viernes))
print(*viernes, sep='\n')