import random
from faker import Faker
from datetime import datetime, timedelta
import uuid

fake = Faker('es_ES')

# Proporciones reales de tipos de sangre en Colombia
tipos_sangre = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-']
probabilidades = [0.56, 0.26, 0.07, 0.02, 0.05, 0.03, 0.007, 0.003]

# Peso promedio (kg) por rango de edad y género para Colombia
peso_por_edad_genero = {
    "Masculino": [
        ((0, 1), 10, 2),
        ((2, 5), 16, 3),
        ((6, 12), 32, 6),
        ((13, 18), 58, 10),
        ((19, 40), 72, 12),
        ((41, 60), 76, 14),
        ((61, 100), 73, 15)
    ],
    "Femenino": [
        ((0, 1), 9, 1.8),
        ((2, 5), 15, 2.8),
        ((6, 12), 28, 5),
        ((13, 18), 55, 9),
        ((19, 40), 65, 10),
        ((41, 60), 70, 13),
        ((61, 100), 68, 14)
    ]
}

def peso_segun_edad_genero(edad, genero):
    rangos = peso_por_edad_genero[genero]
    for (min_edad, max_edad), peso_prom, desv in rangos:
        if min_edad <= edad <= max_edad:
            peso = max(1, round(random.gauss(peso_prom, desv), 1))
            return peso
    return max(1, round(random.gauss(70, 15), 1))

def generar_signos_vitales(edad, peso):
    temp = round(random.uniform(35.1, 39.2), 1)

    aumento_temp = temp > 37.5
    baja_temp = temp < 36.0

    # Frecuencia cardiaca
    if edad <= 1:
        fc_min, fc_max = (100, 160)
    elif edad <= 5:
        fc_min, fc_max = (90, 140)
    elif edad <= 12:
        fc_min, fc_max = (70, 120)
    else:
        fc_min, fc_max = (60, 100)

    if aumento_temp:
        fc = random.randint(fc_min + 10, fc_max + 10)
    elif baja_temp:
        fc = random.randint(fc_min - 10, fc_max - 10)
    else:
        fc = random.randint(fc_min, fc_max)

    # Frecuencia respiratoria
    if edad <= 1:
        fr_min, fr_max = (30, 60)
    elif edad <= 5:
        fr_min, fr_max = (20, 40)
    elif edad <= 12:
        fr_min, fr_max = (18, 30)
    else:
        fr_min, fr_max = (12, 20)

    if aumento_temp:
        fr = random.randint(fr_min + 5, fr_max + 5)
    elif baja_temp:
        fr = random.randint(fr_min - 5, fr_max - 5)
    else:
        fr = random.randint(fr_min, fr_max)

    # Presión arterial
    if edad < 18:
        sis_min, sis_max = (90, 110)
        dias_min, dias_max = (60, 70)
    elif edad < 40:
        sis_min, sis_max = (110, 130)
        dias_min, dias_max = (70, 85)
    else:
        sis_min, sis_max = (120, 150)
        dias_min, dias_max = (75, 95)

    if aumento_temp:
        sis = random.randint(sis_min + 5, sis_max + 5)
        dias = random.randint(dias_min + 3, dias_max + 3)
    elif baja_temp:
        sis = random.randint(sis_min - 5, sis_max - 5)
        dias = random.randint(dias_min - 3, dias_max - 3)
    else:
        sis = random.randint(sis_min, sis_max)
        dias = random.randint(dias_min, dias_max)

    return temp, (sis, dias), fc, fr

def evaluar_frecuencia_cardiaca(fc, edad):
    if edad <= 1:
        if fc < 100: return "Bradicardia"
        if fc > 160: return "Taquicardia"
    elif edad <= 5:
        if fc < 90: return "Bradicardia"
        if fc > 140: return "Taquicardia"
    elif edad <= 12:
        if fc < 70: return "Bradicardia"
        if fc > 120: return "Taquicardia"
    elif edad <= 18:
        if fc < 60: return "Bradicardia"
        if fc > 100: return "Taquicardia"
    else:
        if fc < 60: return "Bradicardia"
        if fc > 100: return "Taquicardia"
    return "Normal"

def evaluar_presion_arterial(sis, dias, edad):
    if edad < 1:
        if sis < 70 or dias < 50: return "Hipotensión"
        if sis > 100 or dias > 65: return "Hipertensión"
    elif edad <= 5:
        if sis < 80 or dias < 55: return "Hipotensión"
        if sis > 110 or dias > 75: return "Hipertensión"
    elif edad <= 12:
        if sis < 90 or dias < 60: return "Hipotensión"
        if sis > 120 or dias > 80: return "Hipertensión"
    elif edad <= 18:
        if sis < 100 or dias < 65: return "Hipotensión"
        if sis > 130 or dias > 85: return "Hipertensión"
    else:
        if sis < 90 or dias < 60: return "Hipotensión"
        if sis > 140 or dias > 90: return "Hipertensión"
    return "Normal"

def evaluar_temperatura(temp):
    if temp < 36.0: return "Hipotermia"
    if temp > 37.5: return "Fiebre"
    return "Normal"

def generar_edad():
    return random.randint(0, 100)

def asignar_fumador(edad, genero):
    if edad < 12: return "No"
    if genero == "Masculino":
        if 12 <= edad <= 24: prob = 0.186
        elif 25 <= edad <= 44: prob = 0.132
        elif 45 <= edad <= 64: prob = 0.117
        else: prob = 0.062
    else:
        if 12 <= edad <= 24: prob = 0.08
        elif 25 <= edad <= 44: prob = 0.055
        elif 45 <= edad <= 64: prob = 0.05
        else: prob = 0.03
    return "Sí" if random.random() < prob else "No"

def asignar_consumo_alcohol(edad, genero):
    if genero == "Masculino":
        if 12 <= edad <= 17: prob = 0.35
        elif 18 <= edad <= 24: prob = 0.60
        elif 25 <= edad <= 44: prob = 0.70
        elif 45 <= edad <= 64: prob = 0.65
        elif edad >= 65: prob = 0.45
        else: prob = 0.01
    else:
        if 12 <= edad <= 17: prob = 0.29
        elif 18 <= edad <= 24: prob = 0.48
        elif 25 <= edad <= 44: prob = 0.58
        elif 45 <= edad <= 64: prob = 0.52
        elif edad >= 65: prob = 0.35
        else: prob = 0.01
    return "Sí" if random.random() < prob else "No"

def edad_ALL(n):
    pico1 = [random.gauss(3.5, 1.0) for _ in range(int(n * 0.6))]
    pico2 = [random.gauss(55, 5.0) for _ in range(n - int(n * 0.6))]

    edades = pico1 + pico2

    edades = [max(0, min(100, e)) for e in edades]  # limitar a 0-100
    random.shuffle(edades)
    return edades

def generar_datos_pacientes(num=100):
    datos = []

    edades_diagnostico = edad_ALL(num)

    for i in range(num):
        genero = random.choice(["Masculino", "Femenino"])
        edad = generar_edad()

        if genero == "Masculino":
            altura = round(random.gauss(171, 7), 1)
            nombre = fake.first_name_male()
        else:
            altura = round(random.gauss(158, 6), 1)
            nombre = fake.first_name_female()

        peso = peso_segun_edad_genero(edad, genero)

        apellido = fake.last_name()
        fecha_consulta = fake.date_between(start_date='-6M', end_date='today')
        tipo_visita = random.choice(["Consulta general", "Control", "Urgencia", "Especialista"])
        proxima_cita = fecha_consulta + timedelta(days=random.randint(7, 60))

        temp, (sis, dias), fc, fr = generar_signos_vitales(edad, peso)
        tipo_sangre = random.choices(tipos_sangre, probabilidades)[0]
        fumador = asignar_fumador(edad, genero)

        datos.append({
            "ID Paciente": str(uuid.uuid4()),
            "Nombre": nombre,
            "Apellido": apellido,
            "Género": genero,
            "Edad": edad,
            "Altura (cm)": altura,
            "Peso (kg)": peso,
            "Temperatura (°C)": temp,
            "Evaluación Temperatura": evaluar_temperatura(temp),
            "Presión Sistólica": sis,
            "Presión Diastólica": dias,
            "Evaluación Presión": evaluar_presion_arterial(sis, dias, edad),
            "Frecuencia Cardíaca (lpm)": fc,
            "Evaluación FC": evaluar_frecuencia_cardiaca(fc, edad),
            "Frecuencia Respiratoria (rpm)": fr,
            "Tipo de Sangre": tipo_sangre,
            "Fumador": fumador,
            "Consume Alcohol": asignar_consumo_alcohol(edad, genero),
            "Edad de diagnóstico ALL (años)": round(edades_diagnostico[i], 1),
            "ID Consulta": str(uuid.uuid4()),
            "Fecha de Consulta": fecha_consulta.strftime('%Y-%m-%d'),
            "Tipo de Visita": tipo_visita,
            "Próxima Cita": proxima_cita.strftime('%Y-%m-%d')
        })

    return datos