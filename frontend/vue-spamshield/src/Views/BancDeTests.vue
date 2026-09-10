<template>
    <main>
        <section class="card-deco">
            <div class="cards">
                <div class="card">
                    <h4>À quoi sert cette section ?</h4>
                    <p>Testez le comportement de SpamShield à l'aide d'un formulaire de simulation. Vous pouvez vérifier votre configuration, identifier d'éventuelles erreurs et soumettre des cas spécifiques afin d'améliorer la détection.</p>
                </div>
            </div>
        </section>
        <section class="formulaire-test card-deco">
            <div class="title">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-robot" viewBox="0 0 16 16">
                    <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>
                    <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>
                </svg>
                <h3>Formulaire de simulation</h3>
            </div>
            <form @submit.prevent="test_new_message">
                <div class="form-fields">
                    <div class="nom-et-prenom">
                        <fieldset>
                            <label>Nom</label>
                            <input type="text" v-model="data.metadata.surname">
                        </fieldset>
                        <fieldset>
                            <label>Prénom</label>
                            <input type="text" v-model="data.metadata.name">
                        </fieldset>
                    </div>
                    <div class="email-et-telephone">
                        <fieldset>
                            <label>E-mail</label>
                            <input type="text" v-model="data.metadata.email">
                        </fieldset>
                        <fieldset>
                            <label>Téléphone</label>
                            <input type="text" class="numero" v-model="data.metadata.phone">
                        </fieldset>
                    </div>
                    <div class="objet">
                        <fieldset class="objet">
                            <label for="object">Objet</label>
                            <input type="text" v-model="data.metadata.subject">
                        </fieldset>
                    </div>
                    <div class="message">
                        <fieldset class="message">
                            <label for="message">Message</label>
                            <textarea name="message" id="message" v-model="data.text">
                            </textarea>
                        </fieldset>
                        
                    </div>
                </div>
                <button type="submit" :disabled="envoiMessageEnCours">
                    {{ envoiMessageEnCours ? "Envoi..." : "Envoyer" }}
                </button>
                <p v-if="statutMessage" class="statut-message">{{ statutMessage }}</p>
            </form>
        </section>
        <section class="inport-data-test card-deco" style="position: relative;">
            <h3>Insérer un fichier JSON de simulation</h3>
            <input type="file" id="messagesJson" accept=".json,application/json" @change="select_json_file">
            <button type="button" @click="send_json_messages" :disabled="envoiEnCours">{{ envoiEnCours ? "Envoi en cours..." : "Envoyer" }}</button>
            <div v-if="envoiEnCours || progression > 0" class="progression-import">
                <p>Message {{ messageActuel }} / {{ totalMessages }}</p>
                <progress :value="progression" max="100"></progress>
                <p>{{ progression }} %</p>
                <p v-if="messageEnCours">Envoi : {{ messageEnCours }}</p>
            </div>
        </section>
    </main>
</template>

<script>
import api from "../axios/axios.js";
export default{
    data(){
        return{
            entrainementModel : true,
            recevoirParMail: true,
            data : {
                metadata : {
                    name : '',
                    surname : '',
                    subject : '- TEST -  ',
                    email : '',
                    phone : '',
                    form_id : 'test'
                },
                text : ''
            },
            jsonFile: null,
            envoiEnCours: false,
            messageActuel: 0,
            totalMessages: 0,
            progression: 0,
            messageEnCours: "",
            envoiMessageEnCours: false,
            statutMessage: "",
        }
    },
    methods:{
        reset_form(){
            this.data = {
                metadata : {
                    name : '',
                    surname : '',
                    subject : '- TEST -  ',
                    email : '',
                    phone : '',
                    form_id : 'test'
                },
                text : ''
            }
        },
        async test_new_message(){
            const data = {
                message : this.data.text,
                metadata : this.data.metadata,
                settings : {
                    entrainementModel : this.entrainementModel,
                    recevoirParMail : this.recevoirParMail
                }
            }

            try {
                this.envoiMessageEnCours = true
                this.statutMessage = "Envoi du message..."
                const result = await api.post("/new-message", data)
                console.log(result)
                this.reset_form()
                this.statutMessage = "Message envoyé avec succès ✅"
            } 
            catch(error) {
                console.error(error)
                this.statutMessage = "Erreur pendant l'envoi du message ❌"
            } 
            finally {
                this.envoiMessageEnCours = false
            }
        },

        select_json_file(event){
            this.jsonFile = event.target.files[0]
            this.messageActuel = 0
            this.totalMessages = 0
            this.progression = 0
            this.messageEnCours = ""
        },


        async send_json_messages(){
            if(!this.jsonFile){
                alert("Sélectionnez d'abord un fichier JSON")
                return
            }

            try {
                const fileText = await this.jsonFile.text()
                const messages = JSON.parse(fileText)
                if(!Array.isArray(messages)){
                    throw new Error("Le fichier JSON doit contenir une liste de messages")
                }


                this.envoiEnCours = true
                this.totalMessages = messages.length
                this.messageActuel = 0
                this.progression = 0
                this.messageEnCours = ""

                for(let i = 0; i < messages.length; i++){
                    const message = messages[i]
                    this.messageActuel = i + 1
                    this.messageEnCours = message.text
                    const data = {
                        message : message.text,
                        metadata : message.metadata,
                        settings : {
                            entrainementModel : this.entrainementModel,
                            recevoirParMail : this.recevoirParMail
                        }
                    }

                    console.log(`Envoi ${i + 1}/${messages.length}`, message.text)

                    await api.post("/new-message", data)

                    this.progression = Math.round(((i + 1) / messages.length) * 100)

                }

                this.envoiEnCours = false
                this.messageEnCours = ""

                alert(`${messages.length} messages envoyés avec succès`)
            } 
            catch(error) {
                console.error(error)
                this.envoiEnCours = false
                alert("Erreur pendant l'import du fichier JSON")
            }
        },

    }
}
</script>

<style scoped>
main{
    display: flex;
    flex-direction: column;
    gap: 10px;
}
section{
    padding: 10px 20px;
    padding-bottom: 30px;
    width: 800px;
    margin-right: auto;
    margin-left: auto;
}

div.cards{
    display: grid;
    gap: 10px;
    margin-top: 20px;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    color: #65639B;

}
div.card{
    /* min-height: 200px; */
    background-color: #F7F8FC;
    padding: 10px;
    position: relative;
    padding-bottom: 50px;
}

h4{
    margin-bottom: 20px;
    font-size: 16px;
    font-weight: 900;
    opacity: 0.6;
}

p{
    font-size: 16px;
}

input[type="checkbox"]{
    position: absolute;
    right: 15px;
    bottom: 10px;
}


/* FORM */

div.title{
    margin-top: 10px;
}

div.title h3{
    font-size: 16px;
}


form{
    padding: 20px;
    position: relative;
    padding-bottom: 60px;
    padding-top: 50px;
    
}

form input[type="text"]{
    border:  #03005b5b 1px solid;
    border-radius: 5px;
    height: 35px;
    margin-bottom: 20px;
}
form div.nom-et-prenom,div.email-et-telephone{
    display: flex;
    gap: 25px;
}

form div.nom-et-prenom input{
    width: 300px;
}
form div.email-et-telephone input{
    width: 300px;
}


form label{
    font-size: 14px;
    font-weight: 800;
    opacity: 0.6;
    margin-bottom: 5px;
}

form textarea{
    height: 200px;
    border:  #03005b5b 1px solid;
    border-radius: 5px;

}


fieldset{
    display: flex;
    flex-direction: column;
    
}

form div.form-fields{
    display: flex;
    flex-direction: column;
    gap: 15px;
}

button{
    position: absolute;
    right: 10px;
    bottom: 10px;
}


</style>