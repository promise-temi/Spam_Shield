import os
import logging
from dotenv import load_dotenv
load_dotenv()
import smtplib
from email.message import EmailMessage
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Database import Postgres_DB
from LLModel import LLMModel


class Mail_Operations:
    def __init__(self):
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.DB = Postgres_DB()
        self.prospects = self.DB.get_prospect_mail('email')
        print(self.prospects)


    def send_mail(self, message, metadata, confidence_score, label):
        logging.info('Début Envoi')
        for mail in self.prospects:
            logging.info('Envoie du message')
            msg = EmailMessage()
            msg["From"] = self.email_address
            msg["To"] = mail
            msg["Subject"] = f"SpamShield {label} - Nouveau message {(' : ' + metadata['subject']) if metadata['subject'] else ''}"
            msg.set_content(f"""Nom : {metadata['surname'] if metadata['surname'] else '__'}\nPrenom : {metadata['name'] if metadata['name'] else '__'}\nEmail : {metadata['email'] if metadata['email'] else '__'}\nTelephone : {metadata['phone'] if metadata['phone'] else '__'}\n\n\n{str(message)}\nConfidence : {confidence_score}\n\n\n\n\nCe type de messages ne vous semble pas pertinant? Aidez Spamshield à mieux comprendre vos besoins. Consulter votre tableau de bord SpamShield pour ajuster vos préférences et affiner les prochaines analyses""")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
            logging.info('Message envoyé avec succès')
        logging.info('Fin Envoi')


    def get_total_messages(self):
        total_messages = self.DB.get_total_messages()
        return total_messages
    
    def get_total_spam(self):
        total_spam = self.DB.get_total_spam()
        return total_spam
    
    def get_total_ham(self):
        total_ham = self.DB.get_total_ham()
        return total_ham
    
    def get_total_spam_rules(self):
        total_spam_rules = self.DB.get_total_spam_rules()
        return total_spam_rules
    
    def get_mean_confidence_score(self):
        mean_confidence_score = self.DB.get_mean_confidence_score()
        return mean_confidence_score
    def get_mean_confidence_score_spam(self):
        mean_confidence_score_spam = self.DB.get_mean_confidence_score_spam()
        return mean_confidence_score_spam
    
    def get_mean_confidence_score_ham(self):
        mean_confidence_score_ham = self.DB.get_mean_confidence_score_ham()
        return mean_confidence_score_ham
    
    def get_banned_patterns_found_count(self):
        banned_patterns_found_count = self.DB.get_banned_patterns_found_count()
        return banned_patterns_found_count
        

    
    

    def send_report(self, phase_start, phase_end, deadline):
        try:
            logging.info("Début Envoi Rapport")

            prospects = self.DB.get_prospect_mail("email")
            logging.info(f"Destinataires rapport : {prospects}")

            if not prospects:
                logging.warning("Aucun destinataire trouvé pour le rapport.")
                return

            llm_report = LLMModel().generate_report_mistral()

            llm_response = llm_report.get("llm_response", "Analyse indisponible.")

            base_metrics = llm_report.get("base_metrics", {})

            system_data = base_metrics.get("system_data", {})
            system_metrics = system_data.get("metrics", {})

            model_metrics = base_metrics.get("model_metrics") or {}
        except AttributeError:
            logging.info("Aucun rapport à envoyer")

        def format_percent(value):
            if value is None:
                return "Non disponible"
            return f"{value * 100:.0f}%"

        messages = system_metrics.get("messages")
        legitimes = system_metrics.get("legitimes")
        indesirables = system_metrics.get("indesirables")
        corrections = system_metrics.get("corrections")
        reclassements = system_metrics.get("reclassements")

        avg_confidence = format_percent(
            system_metrics.get("avg_confidence")
        )

        correction_rate = format_percent(
            system_metrics.get("correction_rate")
        )

        override_rate = format_percent(
            system_metrics.get("override_rate")
        )

        accuracy = format_percent(
            model_metrics.get("accuracy")
        )

        precision = format_percent(
            model_metrics.get("precision")
        )

        recall = format_percent(
            model_metrics.get("recall")
        )

        f1_score = format_percent(
            model_metrics.get("f1_score")
        )

        training_nb = model_metrics.get("training_nb")

        for mail in prospects:
            logging.info(f"Envoi du rapport à : {mail}")

            msg = EmailMessage()

            msg["From"] = self.email_address
            msg["To"] = mail
            msg["Subject"] = "SpamShield - Votre rapport d'activité"

            # Version texte de secours
            msg.set_content(
                f"""Bonjour,

    Voici votre rapport SpamShield pour la période du {phase_start} au {phase_end}.

    Analyse de SpamShield Advisor :

    {llm_response}


    ACTIVITÉ OBSERVÉE

    Messages analysés : {messages if messages is not None else "Non disponible"}
    Messages légitimes : {legitimes if legitimes is not None else "Non disponible"}
    Messages indésirables : {indesirables if indesirables is not None else "Non disponible"}
    Corrections humaines : {corrections if corrections is not None else "Non disponible"}
    Reclassements automatiques : {reclassements if reclassements is not None else "Non disponible"}

    Confiance moyenne : {avg_confidence}
    Taux de correction : {correction_rate}
    Taux d'override : {override_rate}


    PERFORMANCES DU MODÈLE

    Accuracy : {accuracy}
    Précision : {precision}
    Rappel : {recall}
    F1-score : {f1_score}
    Nombre d'exemples d'entraînement : {training_nb if training_nb is not None else "Non disponible"}


    Vous avez jusqu'au {deadline} pour vérifier et corriger les messages avant leur suppression définitive.

    À bientôt,

    SpamShield
    """
            )

            html = f"""
            <html>
            <body style="
                margin: 0;
                padding: 30px;
                background-color: #f5f6f8;
                font-family: Arial, sans-serif;
                color: #222;
            ">

                <div style="
                    max-width: 700px;
                    margin: auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 12px;
                ">

                    <h1 style="
                        margin-top: 0;
                        margin-bottom: 20px;
                    ">
                        Rapport SpamShield
                    </h1>

                    <p>Bonjour,</p>

                    <p style="line-height: 1.6;">
                        Voici votre rapport SpamShield pour la période
                        <strong>{phase_start}</strong> au
                        <strong>{phase_end}</strong>.
                    </p>

                    <h2 style="margin-top: 30px;">
                        Analyse de SpamShield Advisor
                    </h2>

                    <div style="
                        background-color: #f5f6f8;
                        padding: 18px;
                        border-radius: 8px;
                        white-space: pre-wrap;
                        line-height: 1.6;
                    ">
                        {llm_response}
                    </div>

                    <h2 style="margin-top: 30px;">
                        Activité observée
                    </h2>

                    <table style="
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    ">

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Messages analysés
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>
                                    {messages if messages is not None else "Non disponible"}
                                </strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Messages légitimes
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>
                                    {legitimes if legitimes is not None else "Non disponible"}
                                </strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Messages indésirables
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>
                                    {indesirables if indesirables is not None else "Non disponible"}
                                </strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Corrections humaines
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>
                                    {corrections if corrections is not None else "Non disponible"}
                                </strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Reclassements automatiques
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>
                                    {reclassements if reclassements is not None else "Non disponible"}
                                </strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Confiance moyenne
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>{avg_confidence}</strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Taux de correction
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>{correction_rate}</strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Taux d'override
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>{override_rate}</strong>
                            </td>
                        </tr>

                    </table>

                    <h2 style="margin-top: 30px;">
                        Performances du modèle
                    </h2>

                    <table style="
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    ">

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Accuracy
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>{accuracy}</strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Précision
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>{precision}</strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Rappel
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>{recall}</strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                F1-score
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>{f1_score}</strong>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                                Exemples utilisés à l'entraînement
                            </td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd; text-align: right;">
                                <strong>
                                    {training_nb if training_nb is not None else "Non disponible"}
                                </strong>
                            </td>
                        </tr>

                    </table>

                    <div style="
                        margin-top: 30px;
                        padding: 15px;
                        background-color: #fff7e6;
                        border-radius: 8px;
                        line-height: 1.5;
                    ">
                        Vous avez jusqu'au
                        <strong>{deadline}</strong>
                        pour vérifier et corriger les messages avant leur suppression définitive.
                    </div>

                    <p style="
                        margin-top: 30px;
                        line-height: 1.5;
                    ">
                        À bientôt,<br>
                        <strong>SpamShield</strong>
                    </p>

                </div>

            </body>
            </html>
            """

            msg.add_alternative(
                html,
                subtype="html"
            )

            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465
            ) as smtp:

                smtp.login(
                    self.email_address,
                    self.email_password
                )

                smtp.send_message(msg)

            logging.info(
                f"Rapport envoyé avec succès à {mail}"
            )

        logging.info("Fin Envoi Rapport")