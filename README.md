# Proyecto final de AREP
# Medical Data Generator
## Integrantes

- Laura Daniela Rodríguez Sánchez
- Juan David Martínez Méndez
- Santiago Gualdrón Rincón

## Prerrequisitos

Para el correcto uso del servicio, es necesario tener las siguientes aplicaciones instaladas:
- PYTHON
     ```sh
   python3 --version
   ```
- GIT
   ```sh
   git --version
   ```
(NOTA: si alguna de estas aplicaciones no fue instalada, ir a la página oficial de cada una e instalar la versión recomendada).

### Instalación
1. clonar el repositorio con el siguiente comando y ingresar a la carpeta en donde esta incluido el codigo:

   ```sh
   git clone https://github.com/Fataltester/Proyecto_AREP.git
   cd Proyecto_AREP
   ```

---

## 🧬 Introducción
Este proyecto es un **generador de datos sintéticos** diseñado para el contexto de la **simulación de historias clínicas y registros médicos**.  
El sistema crea datasets estructurados y pseudorandomizados que imitan características reales de consultas médicas.  
El generador soporta una cantidad variable de filas y produce datos que siguen **restricciones, distribuciones y tendencias reales**.

---

## 📚 Datos Reales Utilizados

Esta sección presenta los datos reales usados como referencia para la generación del dataset sintético.  
En varios casos, la información proviene de registros públicos de Colombia.  
El objetivo es asegurar que los datos generados reflejen adecuadamente condiciones demográficas y clínicas reales.

---

## 🇨🇴 Resultados y Comparación con Datos de Colombia

A continuación se presenta información real usada como referencia para validar las variables generadas por el sistema.

---

### 1. **Distribución de Tipos de Sangre en Colombia**

| Tipo de Sangre | % Real (DANE/INS) |
|----------------|--------------------|
| O+             | 56%                |
| A+             | 26%                |
| B+             | 7%                 |
| AB+            | 2%                 |
| O−             | 5%                 |
| A−             | 3%                 |
| B−             | 0.7%               |
| AB−            | 0.3%               |

---

### 2. **Estatura Promedio en Colombia**

| Género | Estatura Promedio (cm) |
|--------|--------------------------|
| Hombre | 171.9                   |
| Mujer  | 158                     |

---

### 3. **Peso Promedio por Edad en Colombia**

| Rango de Edad | Peso Promedio (kg) |
|----------------|--------------------|
| 0–18           | 40.5               |
| 19–40          | 67.5               |
| 41–65          | 70.2               |
| 66+            | 65.4               |

---

### 4. **Tasa de Fumadores por Género (ENS 2020)**

| Género | % Fumadores |
|--------|-------------|
| Hombre | 16.9%       |
| Mujer  | 7.6%        |

---

### 5. **Tasa de Fumadores por Edad**

| Edad | % Fumadores |
|------|-------------|
| 12–24 | 18.6%      |
| 25–44 | 13.2%      |
| 45–64 | 11.7%      |
| 65+   | 6.2%       |

---

### 6. **Consumo de Alcohol en Colombia (ENS 2020)**

| Género | % Consumidores |
|--------|----------------|
| Hombre | 58.1%          |
| Mujer  | 41.9%          |

---

### 7. **Frecuencia Cardíaca por Edad (bpm en reposo)**

| Edad | Rango Normal | Promedio Real |
|------|--------------|----------------|
| 0–18 | 70–100       | 85             |
| 19–40 | 60–100       | 76             |
| 41–65 | 60–100       | 75             |
| 66+   | 60–100       | 73             |

---

### 8. **Frecuencia Respiratoria por Edad**

| Edad | Rango Normal | Promedio Real |
|------|--------------|----------------|
| 0–18 | 16–22        | 18             |
| 19–40 | 12–20        | 16             |
| 41–65 | 12–20        | 16             |
| 66+   | 12–20        | 17             |

---

### 9. **Presión Arterial Sistólica por Edad (mmHg)**

| Edad | Rango Normal | Promedio Real |
|------|--------------|----------------|
| 0–18 | 90–120       | 110            |
| 19–40 | 110–130      | 120            |
| 41–65 | 115–140      | 130            |
| 66+   | 120–150      | 138            |

---

# 🚀 Pruebas de Rendimiento y Validación del Prototipo en AWS

Esta sección documenta las pruebas de rendimiento, pruebas de carga y validación del prototipo en AWS, realizadas para evaluar la estabilidad, eficiencia y escalabilidad del generador en un entorno real de despliegue.

---

## 🔥 Prueba de Carga con k6

Se diseñó un script de pruebas usando **k6**, orientado a evaluar:

- Latencia
- Tasa de éxito
- Estabilidad bajo carga
- Variación por tamaño del dataset generado

### 🎯 Estrategia de la Prueba

El escenario utilizó tres etapas:

1. **Ramp-up:** 30 s → 5 usuarios
2. **Carga sostenida:** 1 min → 20 usuarios
3. **Ramp-down:** 30 s → 0 usuarios

Se definió un **umbral de rendimiento**:

> El 95% de las solicitudes debe completarse en < 500 ms.

### 🧪 Lógica del Test

Cada usuario virtual solicita datasets de:

`50, 100, 200, 400 y 700` registros.

En cada ciclo:

- Se hace una petición GET al endpoint `/generate`.
- Se verifica que el código de respuesta sea **200**.
- Se espera 1 segundo antes de la siguiente solicitud.

---

# 📊 Resultados de la Prueba de Carga con k6

### ✔️ Resumen General

| Métrica | Valor |
|--------|--------|
| **Checks (status 200)** | 60% (219 ✓ / 146 ✗) |
| **Solicitudes totales** | 365 |
| **Tasa de solicitudes** | 2.78 req/s |
| **Iteraciones** | 73 |
| **Usuarios virtuales** | 1–20 |
| **VUs máximos** | 20 |

---

### 📡 Tráfico

| Métrica | Valor |
|--------|--------|
| **Datos recibidos** | 18 MB (138 kB/s) |
| **Datos enviados** | 81 kB (618 B/s) |

---

### 🔌 Conexión y Bloqueo

| Métrica | Prom | Min | Med | Máx | p(90) | p(95) |
|--------|------|------|------|-------|--------|--------|
| http_req_blocked | 8.93 ms | 100 ns | 0.4 µs | 324.92 ms | 1.46 µs | 143.02 ms |
| http_req_connecting | 4.12 ms | 0 ms | 0 ms | 94.25 ms | 0 ms | 70.51 ms |
| TLS handshaking | 4.32 ms | 0 ms | 0 ms | 116.52 ms | 0 ms | 71.62 ms |

---

### ⏱️ Duración de Solicitudes

| Métrica | Prom | Min | Med | Máx | p(90) | p(95) |
|--------|------|------|-------|-------|--------|--------|
| http_req_duration | 2.44 s | 633 ms | 2.36 s | 4.4 s | 3.84 s | 3.86 s |
| expected_response: true | 1.77 s | 633 ms | 1.68 s | 3.64 s | 3.12 s | 3.32 s |
| http_req_waiting | 2.40 s | 587 ms | 2.21 s | 4.4 s | 3.84 s | 3.86 s |

---

### 🔁 Duración de Iteraciones

| Métrica | Valor |
|--------|--------|
| Promedio | 17.28 s |
| Mínimo | 15.42 s |
| Máximo | 19.42 s |
| p(90) | 18.58 s |
| p(95) | 19.06 s |

---

# 📈 Interpretación de los Resultados

### 1. **Tasa de éxito (60%)**
Una tasa de fallos del 40% indica **inestabilidad** del servicio ante cargas crecientes o datasets grandes.

### 2. **Latencias elevadas**
El p95 ≈ 3.86 s demuestra que la API **no cumple el objetivo de < 500 ms**.

### 3. **Cuello de botella interno**
El tiempo de espera (`waiting`) ≈ duración total confirma que el retraso ocurre **en el procesamiento de datos**, no en la red.

### 4. **Conectividad estable**
Las métricas de envío, recepción y conexión muestran tiempos normales.

### 5. **Procesamiento costoso**
Las iteraciones tardan entre 17–19 segundos, consistente con solicitudes de alto costo.

---

# 🧪 Conclusiones Generales

- La API responde bien con carga baja, pero experimenta **fallos y lentitud** con solicitudes grandes o múltiples usuarios.
- El principal problema es el **costo computacional de generar datos sintéticos extensos**.
- La arquitectura puede mejorar si se aplican optimizaciones como:

    - Mayor memoria/CPU en Lambda
    - Límites más bajos para `count`
    - Generación en paralelo
    - Procesamiento asíncrono
    - Servicios más robustos (ECS, EC2)

---

# 🎥 Prototipo

📺 Video demostrativo del funcionamiento:

**Link**: https://youtu.be/VW9wmDOxI5I

[![VideoPrototipo](https://img.youtube.com/vi/VW9wmDOxI5I/0.jpg)](https://www.youtube.com/watch?v=VW9wmDOxI5I)

## Construido con

[Git](https://git-scm.com) - Version Control System

[Python](https://www.python.org/) - Python file script

## Autor

Laura Daniela Rodríguez Sánchez - [LauraRo166](https://github.com/LauraRo166)

Juan David Martínez Méndez - [Fataltester](https://github.com/Fataltester)

Santiago Gualdron Rincon - [Waldron63](https://github.com/Waldron63)
