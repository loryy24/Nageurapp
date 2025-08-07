import random
import time
from datetime import datetime
import threading
from .models import db  # ⚠️ À adapter si l'import ne fonctionne pas selon ton arborescence
from flask import current_app

data_buffer = []
simulating = True

def simulate_data():
    with current_app.app_context():  # On exécute dans le contexte Flask
        while simulating:
            bpm = random.randint(50, 120)
            new_data = {
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'batt_level': round(random.uniform(20.0, 100.0), 2),
                'temp': round(random.uniform(36.0, 39.0), 2),
                'pulse': bpm,
                'distance': round(random.uniform(10.0, 50.0), 2),
            }

            # Ajouter dans le buffer
            data_buffer.append(new_data)
            if len(data_buffer) > 100:
                data_buffer.pop(0)

            # Sauvegarde dans la base
            db.session.commit()

            time.sleep(2)
