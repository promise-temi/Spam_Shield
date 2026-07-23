import pandas as pd
import os
import logging
import kagglehub


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




class SET_Spam_Shield_Dependances:
    def __init__(self, raw_data_dir=""):
        self.raw_data_dir = raw_data_dir
        self.final_df = []

    

    def Dependances_Full_Pipeline(self, lang):
        """
        Retourne un dataframe apres avoir réccupéré les données dont le projet a besoin
        """
        logging.info('Début du téléchargement des données')
        self.Multiligual_Spam_Dataset()
        self.Professionnal_mails_fr()
        self.SMS_spam_detection_multilingual()
        logging.info('Fin du téléchargement des données')
        logging.info('Concaténation des données en dataset exploitable')
        df = self.get_inatial_df(lang)
        return df


    def __create_dir_if_not_exist(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)





        



    def Multiligual_Spam_Dataset(self):
        # telechargement initial du dataset
        output_dir = f"{self.raw_data_dir}/multiligual_spam_dataset"
        kagglehub.dataset_download("rajnathpatel/multilingual-spam-data", output_dir=output_dir)
        

        # reccupération du dataset d'interet
        try:
            df = pd.read_csv(f"{output_dir}/data-en-hi-de-fr.csv")
        except Exception as e:
            logging.error(f"Dataset not available : {e}")
            return
        # Identification des livrables d'interets
        interesting_cols = ['labels','text', 'text_fr']
        df_filtered = df[interesting_cols]

        # pre-nettoyage
        df_filtered['labels'] = df_filtered['labels'].replace('spam', 1)
        df_filtered['labels'] = df_filtered['labels'].replace('ham', 0)
        df_filtered['labels'] = df_filtered['labels'].astype(int)
        
        # Messages anglais
        df_filtered_eng = df_filtered[['labels', 'text']]
        df_filtered_eng['lang'] = 'eng'
        df_filtered_eng = df_filtered_eng.rename(columns={'labels':'label'})
        logging.info(f"Multiligual_Spam_Dataset eng - {df_filtered_eng.shape}")
        self.final_df.append(df_filtered_eng)
        
        # Messages Francais
        df_filtered_fr = df_filtered[['labels', 'text_fr']]
        df_filtered_fr['lang'] = 'fr'
        df_filtered_fr = df_filtered_fr.rename(columns={'labels':'label', 'text_fr':'text'})
        logging.info(f"Multiligual_Spam_Dataset fr - {df_filtered_fr.shape}")
        self.final_df.append(df_filtered_fr)
         

    
    def Phishing_Email_Dataset(self):
        output_dir = f"{self.raw_data_dir}/phishing_email_dataset"
        kagglehub.dataset_download("naserabdullahalam/phishing-email-dataset", output_dir=output_dir)

        # pour chaques fichiers
        for file_name in os.listdir(output_dir):
            if file_name == '.complete' :
                continue
            try:
                try:
                    df = pd.read_csv(f'{output_dir}/{file_name}')
                except Exception as e:
                    logging.error(f"Dataset not available : {e}")
                    return
                interesting_cols = ['label','body']

                #identification des colonnes d'interet
                df_filtered = df[interesting_cols]

                # les messages sont uniquement anglais
                df_filtered = df_filtered.rename(columns={'body':'text'})
                df_filtered['lang'] = 'eng'
                logging.info(f"Phishing_Email_Dataset - {file_name} - {df_filtered.shape}")
                self.final_df.append(df_filtered)
            except Exception as e:
                logging.debug(e)
                continue
                
            


    def Professionnal_mails_fr(self):
        output_dir = f"{self.raw_data_dir}/french_ham_contact_dataset_1000.json"
        self.__create_dir_if_not_exist(output_dir)
        try:
            df = pd.read_json(output_dir)
        except Exception as e:
            logging.error(f"Dataset not available : {e}")
            return

        # les collones sont deja standardisé c'est un dataset custum, réalisé par mes soins
        df['lang'] = 'fr'
        logging.info(f"Professionnal_mails_fr - {df.shape}")
        self.final_df.append(df)
        

    def SMS_spam_detection_multilingual(self):
        output_dir = f"{self.raw_data_dir}/sms_spam_detection_multilingual"
        kagglehub.dataset_download("debapampal2002/sms-dataset1", output_dir=output_dir)

        self.__create_dir_if_not_exist(output_dir)
        try: 
            df = pd.read_csv(f'{output_dir}/dataset.csv')
        except Exception as e:
            logging.error(f"Dataset not available : {e}")
            return
        # idetification des colonnes d'interet
        interesting_cols = ['labels', 'text']

        # netoyage et preparation des messages français
        df_fr = df[(df['lang'] == 'french')]
        df_fr = df_fr[interesting_cols]
        df_fr['lang'] = 'fr'
        df_fr = df_fr.replace({'ham':0, 'spam':1, }).rename(columns={'labels':'label'})
        df_fr['label'] = df_fr['label'].astype(int)
        logging.info(f"SMS_spam_detection_multilingual fr- {df_fr.shape}")
        self.final_df.append(df_fr)

        # netoyage et preparation des messages anglais
        df_eng = df[(df['lang'] == 'english')]
        df_eng = df_eng[interesting_cols]
        df_eng['lang'] = 'eng'
        df_eng = df_eng.replace({'ham':0, 'spam':1, }).rename(columns={'labels':'label'})
        df_eng['label'] = df_eng['label'].astype(int)
        logging.info(f"SMS_spam_detection_multilingual eng - {df_eng.shape}")
        self.final_df.append(df_eng)


    def get_inatial_df(self, lang):
        # creation du dataset final
        df_all = pd.concat(self.final_df)
        df_all = df_all[df_all['lang'] == lang]
        logging.info(f"Global dataframe created - {df_all.shape}")
        return df_all