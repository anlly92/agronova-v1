from datetime import datetime
import pickle
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def obtener_servicio():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        raise Exception("No se encontró token.json. Ejecuta la autenticación manualmente primero.")
    return build("calendar", "v3", credentials=creds)

def listar_eventos(max_results=10):
    servicio = obtener_servicio()
    now = datetime.utcnow().isoformat() + "Z"
    calendar_id ='368f8a72ad09d483503fdaebb646979976b1ea4d077c84b0c0305c9e5f50b799@group.calendar.google.com'
    eventos = (
        servicio.events()
        .list(calendarId=calendar_id, timeMin=now, maxResults=max_results, singleEvents=True, orderBy="startTime")
        .execute()
        .get("items", [])
    )
    return eventos

def crear_evento(title, descripcion, fecha_inicio, fecha_fin):
    servicio = obtener_servicio()
    try:
        dt_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M")
        dt_fin = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M")

        inicio = dt_inicio.isoformat() + "-05:00"
        fin = dt_fin.isoformat() + "-05:00"

    except ValueError as e:
        raise Exception(f"Error al parsear fechas: {e}")

    calendar_id ='368f8a72ad09d483503fdaebb646979976b1ea4d077c84b0c0305c9e5f50b799@group.calendar.google.com'
    evento = {
        "summary": title,
        "description": descripcion,
        "start": {"dateTime": inicio, "timeZone": "America/Bogota"},
        "end": {"dateTime": fin, "timeZone": "America/Bogota"},
    }
    evento_creado = servicio.events().insert(calendarId=calendar_id, body=evento).execute()
    return evento_creado.get("htmlLink")

def eliminar_evento(event_id):
    servicio = obtener_servicio()
    calendar_id = '368f8a72ad09d483503fdaebb646979976b1ea4d077c84b0c0305c9e5f50b799@group.calendar.google.com'
    servicio.events().delete(calendarId=calendar_id, eventId=event_id).execute()

def actualizar_evento(event_id, titulo, descripcion, fecha_inicio, fecha_fin):
    servicio = obtener_servicio()
    calendar_id = '368f8a72ad09d483503fdaebb646979976b1ea4d077c84b0c0305c9e5f50b799@group.calendar.google.com'

    try:
        dt_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%dT%H:%M")
        dt_fin = datetime.strptime(fecha_fin, "%Y-%m-%dT%H:%M")

        inicio = dt_inicio.isoformat() + "-05:00"
        fin = dt_fin.isoformat() + "-05:00"

    except ValueError as e:
        raise Exception(f"Error al parsear fechas: {e}")

    evento = servicio.events().get(
        calendarId=calendar_id, 
        eventId=event_id
        ).execute()

    # Actualizar los campos necesarios
    evento['summary'] = titulo
    evento['description'] = descripcion
    evento['start'] = {'dateTime': inicio,'timeZone': 'America/Bogota',}
    evento['end'] = {'dateTime': fin,'timeZone': 'America/Bogota',}

    # enviar los cambios a google calendar
    actualizado = servicio.events().update(
        calendarId=calendar_id,
        eventId=event_id,
        body=evento
    ).execute()
