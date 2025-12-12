from medicDataGenerator.medicDataGenerator import generar_datos_pacientes
from decimal import Decimal
import boto3
import json
import os


dynamo = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = os.environ["TABLE_NAME"]
TOPIC_ARN = os.environ["TOPIC_ARN"]


def convertir_a_decimal(obj):
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, dict):
        return {k: convertir_a_decimal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convertir_a_decimal(v) for v in obj]
    return obj


def lambda_handler(event, context):
    params = event.get("queryStringParameters", {}) or {}

    count = int(params.get("count", 10))
    email = params.get("email")

    # 1. Generar datos
    datos = generar_datos_pacientes(count)

    # Convertir floats → Decimal
    datos = convertir_a_decimal(datos)

    # 2. Guardar en DynamoDB
    table = dynamo.Table(TABLE_NAME)
    with table.batch_writer() as batch:
        for item in datos:
            batch.put_item(Item=item)

    # 3. Notificación SNS (opcional)
    if email and TOPIC_ARN.startswith("arn:aws:sns"):
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject="Generación completada",
            Message=f"Se generaron {count} registros sintéticos."
        )

    # 4. Respuesta API
    return {
        "statusCode": 200,
        "body": json.dumps({"status": "ok", "rows": count})
    }