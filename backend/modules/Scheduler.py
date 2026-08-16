import os
import sys
import datetime
import logging

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__)
        )
    )
)

from Database import Postgres_DB
from Mail_Operations import Mail_Operations


class Scheduler:

    def __init__(self):
        # TEST : 1 minute de phase
        self.phase_duration = datetime.timedelta(minutes=1)

        # TEST : 1 minute de carence
        self.phase_carence = datetime.timedelta(minutes=1)

        # Envoi du rapport dès le début de la carence
        self.carence_message_delay = datetime.timedelta(seconds=0)

        self.DB = Postgres_DB()
        self.mail_ops = Mail_Operations()

        self.set_new_phase_if_no_phase()


    def get_current_phase(self):
        current_phase = self.DB.get_current_phase()

        logging.info(
            f"Phase actuelle : {current_phase}"
        )

        if current_phase:
            self.check_phase(current_phase)


    def set_new_phase_if_no_phase(self):
        current_phase = self.DB.get_current_phase()

        if not current_phase:
            logging.info(
                "Aucune phase actuelle trouvée. "
                "Création d'une nouvelle phase."
            )

            self.set_new_phase()


    def set_new_phase(self):
        phase_start = datetime.datetime.now()
        phase_end = phase_start + self.phase_duration

        self.DB.set_new_phase(
            phase_start,
            phase_end
        )

        logging.info(
            f"Nouvelle phase créée : "
            f"{phase_start} -> {phase_end}"
        )


    def check_phase(self, checkphase):
        current_date = datetime.datetime.now()

        phase_id = checkphase[0]
        phase_start = checkphase[1]
        phase_end = checkphase[2]

        carence_end = phase_end + self.phase_carence

        # PHASE EN COURS
        
        if current_date <= phase_end:
            logging.info(
                "La phase est toujours en cours."
            )
            return


        # CARENCE EN COURS
        

        if phase_end < current_date < carence_end:
            logging.info(
                "La phase est terminée. "
                "La période de carence est en cours."
            )

            if current_date >= phase_end + self.carence_message_delay:
                logging.info(
                    "Envoi du rapport de fin de phase."
                )
                try:
                    self.mail_ops.send_report(
                        phase_start,
                        phase_end,
                        carence_end
                    )
                except Exception as e:
                    logging.info("Aucune données pour réaliser un rapport")

            return


      
        #  FIN DE CARENCE
       

        if current_date >= carence_end:
            logging.info(
                "La période de carence est terminée."
            )

            logging.info(
                f"Sauvegarde anonymisée des messages "
                f"créés jusqu'au {phase_end} inclus."
            )

            self.DB.save_anonimized_messages(
                before=phase_end
            )

            logging.info(
                f"Suppression des messages "
                f"créés jusqu'au {phase_end} inclus."
            )

            self.DB.delete_phase_messages(
                before=phase_end
            )

            logging.info(
                "Création d'une nouvelle phase."
            )

            self.set_new_phase()