import os
import sys
import datetime
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Database import Postgres_DB
from Mail_Operations import Mail_Operations
class Scheduler():
    def __init__(self):
        self.phase_duration = 7
        self.phase_carence = 7
        self.carence_message_day = 1
        self.DB = Postgres_DB()
        self.mail_ops = Mail_Operations()
        self.set_new_phase_if_no_phase()

    def get_current_phase(self):
        current_phase = self.DB.get_current_phase()
        if current_phase:
            self.check_phase(current_phase)

    def set_new_phase_if_no_phase(self):
        current_phase = self.DB.get_current_phase()
        if not current_phase:
            logging.info("Aucune phase actuelle trouvée. Création d'une nouvelle phase.")
            self.set_new_phase()


    def set_new_phase(self):
        new_phase = datetime.datetime.now()
        end_phase = new_phase + datetime.timedelta(days=self.phase_duration)
        self.DB.set_new_phase(new_phase, end_phase)

    def check_phase(self, checkphase):
        current_date = datetime.datetime.now()
        phase_end = checkphase[2]
        if current_date > phase_end:
            
            if (current_date - phase_end).days < self.phase_carence:
                logging.info("La phase actuelle est terminée. La période de carence n'est pas encore écoulée.")

            if (current_date - phase_end).days < self.carence_message_day:
                logging.info("première journée de carence. Envoi d'un message de rappel aux utilisateurs.")
                self.mail_ops.send_report(checkphase[0], checkphase[1], checkphase[1] + datetime.timedelta(days=self.phase_duration))

            if (current_date - phase_end).days >= self.phase_carence:
                logging.info("La phase actuelle est terminée. Création d'une nouvelle phase.")
                self.set_new_phase()
            


    