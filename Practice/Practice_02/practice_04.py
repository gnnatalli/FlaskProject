""" Задача 4: Модель с расширенной валидацией даты
Создайте модель Appointment для записи на прием, которая включает
patient_name (строка), appointment_date (дата и время) и проверку, что запись
не может быть установлена ранее, чем через 24 часа от текущего момента. """

from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta

class Appointment(BaseModel):
    patient_name: str
    appointment_date: datetime

    @field_validator('appointment_date')
    def check_appointment_date(cls, v):
        if v < datetime.now() + timedelta(days=1):
            raise ValueError("Appointment must be scheduled at least 24 hours in advance.")


try:
    appointment = Appointment(patient_name="John Joe", appointment_date=datetime.now() + timedelta(hours=25))
    print(appointment)
except ValueError as e:
    print(e)
