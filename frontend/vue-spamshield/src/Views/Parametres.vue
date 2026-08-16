<template>
<main>
    <section class="expression-interdites card-deco">
            <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-robot" viewBox="0 0 16 16">
                        <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>
                        <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>
                    </svg>
                    <h3>Expressions interdites</h3>
                </div>
        <div class="cards">
            <div class="card card1">
                <h4>Ajouter une expression interdite</h4>
                <p>Utilisez le format Regex (expression régulière) pour définir les mots ou motifs à détecter automatiquement.</p>
                <p class="alert">Exemple : .*(insulte|injure|mot interdit).*</p>
                <fieldset>
                    <input type="search" id="nouvelle-expression">
                    <button v-on:click="ajouterExpression">Ajouter</button>
                </fieldset>
            </div>
            <div class="card card2">
                <h4>Expressions interdites enregistrés</h4>
                
                <div class="liste_affichages" v-if="expressions">
                    <div v-for="expression in expressions">
                        <p>{{expression.pattern}}</p>
                        <button v-on:click="supprimerExpression(expression.id)">Supprimer</button>
                    </div>
                </div>
                <div v-else >
                    <p>aucune expression enregistrée pour le moment</p>
                </div>
            </div>
        </div>
    </section>
    <section class="destinataires card-deco">
        <div class="title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-robot" viewBox="0 0 16 16">
                <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>
                <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>
            </svg>
            <h3>Destinataires</h3>
        </div>
        
        <div class="cards">
            <div class="card card1">
                <h4>Ajouter un destinataires</h4>
                
                <p>Ajoutez une adresse e-mail pour recevoir les messages légitimes et les rapports SpamShield.</p>
                <fieldset>
                    <input type="search" id="nouveau-destinataire">
                    <button v-on:click="ajouterDestinataires" >Ajouter</button>
                </fieldset>
            </div>
            <div class="card card2">
                <h4>Destinataires enregistrés</h4>
                
                <div class="liste_affichages" v-if="destinataires">
                    <div v-for="destinataire in destinataires">
                        <p>{{destinataire.email}}</p>
                        <button v-on:click="supprimerDestinataires(destinataire.id)">Supprimer</button>
                    </div>
                </div>
                <div v-else >
                    <p>aucun destinataire enregistré pour le moment</p>
                </div>
            </div>
        </div>
    </section>
    <section class="metadonnee-formulaire card-deco">
        <div class="title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-robot" viewBox="0 0 16 16">
                <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>
                <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>
            </svg>
            <h3>Champs obligatoires du formulaire</h3>
        </div>
        <div class="cards">
            <div class="card">
                <h4>Nom obligatoire</h4>
                <p>Exige la saisie du nom dans le formulaire.</p>
                <input type="checkbox" @change="updateFormRequirements('surname')" v-model="formRequirements.surname">
            </div>
            <div class="card">
                <h4>Prenom obligatoire</h4>
                <p>Exige la saisie du Prenom dans le formulaire.</p>
                <input type="checkbox" @change="updateFormRequirements('name')" v-model="formRequirements.name">
            </div>
            <div class="card">
                <h4>Object obligatoire</h4>
                <p>Exige la saisie d'un objet dans le formulaire.</p>
                <input type="checkbox" @change="updateFormRequirements('subject')" v-model="formRequirements.subject">
            </div>
            <div class="card">
                <h4>Adresse e-mail obligatoire</h4>
                <p>Exige la saisie d'une adresse e-mail dans le formulaire</p>
                <input type="checkbox" @change="updateFormRequirements('email')" v-model="formRequirements.email">
            </div>
            <div class="card">
                <h4>Numéro de téléphone obligatoire</h4>
                <p>Exige la saisie d'un numéro de téléphone dans le formulaire.</p>
                <input type="checkbox" @change="updateFormRequirements('phone')" v-model="formRequirements.phone">
            </div>
        </div>
    </section>
    <!-- MODEL IA -->
    <section class="model-ia card-deco">
        <div class="title">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-robot" viewBox="0 0 16 16">
                <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>
                <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>
            </svg>
            <h3>Model IA</h3>
        </div>
        <div class="cards">
            <div class="card card1">
                <ul>
                    <!-- <li>Model : <strong>SVC (Support Vector Classifier)</strong></li> -->
                    <li>Données d'entrainement : <strong>{{ modelInfos.training_nb }}</strong></li>
                    <li>Nouvelle données disponibles: <strong>{{modelInfos.training_data}}</strong></li>
                </ul>
                <div class="card1-lateral">
                    <ul>
                        <li><span>Performance du modèle</span></li>
                        <li>Exactitude : <strong>{{ modelInfos.accuracy.toFixed(2) }} </strong></li>
                        <li>Score F1 :  <strong>{{ modelInfos.f1_score.toFixed(2) }} </strong></li>
                        <li>Précision : <strong>{{ modelInfos.precision.toFixed(2) }} </strong></li>
                        <li>Rappel : <strong>{{ modelInfos.recall.toFixed(2) }} </strong></li>
                    </ul>
                    
                </div>
                <div class="buttons">
                    <button><a href="http://127.0.0.1:5050/#/" target="_blank">ML Flow</a></button>
                    <button><a href="http://127.0.0.1:3000" target="_blank">Grafana</a></button>
                </div>
            </div>
            <div class="card card3">
                <h4>Réentraîner le modèle d'IA</h4>

                <p>
                    Réentraînez le modèle avec les nouvelles données collectées afin d'améliorer
                    progressivement ses performances et de l'adapter aux corrections apportées.
                </p>

                <button v-on:click="retrainModel">
                    Réentraîner le modèle
                </button>
            </div>
            <div class="card card3">
                <h4>Réinitialiser le modèle d'IA</h4>
                <p>Supprimez le modèle actuellement utilisé et revenez à un modèle vierge.</p>
                <p class="alert">Attention — action irréversible<br>Cette action supprimera définitivement le modèle, son historique, ses données d’entraînement et toutes les améliorations acquises. Aucune donnée ne pourra être récupérée.</p>
                <button v-on:click="resetModel">Réinitialiser</button>
            </div>
        </div>
    </section> 
</main>
</template>

<script>
import api from "../axios/axios.js";

export default{
    data(){
        return{
            expressions : null,
            destinataires : null,
            formRequirements : {
                name : false,
                surname : false,
                email : false,
                phone : false,
                subject : false
            },
            modelInfos:{
                accuracy: 0, 
                precision: 0, 
                recall: 0,
                f1_score: 0,
                training_nb: 0,
                training_data:0,
            }
        }
    },
    methods:{
        // EXPRESSIONS
        getAllExpressions(){
            api.get(`/get-regexes`)
            .then(result => {
                console.log("Expressions réccuperées avec succès")
                this.expressions = result.data.regex_rules
            })
            .catch(error => {
                console.error(error)
            })
        },

        ajouterExpression(){
            let pattern = document.querySelector('#nouvelle-expression').value
            let data = {
                pattern : pattern
            }
            api.post(`/new-regex`, data)
            .then(result => {
                console.log(result)
                this.getAllExpressions()
            })
            .catch(error => {
                console.error(error)
            })
        },

        supprimerExpression(id){
            api.delete(`/delete-regex/${id}`)
            .then(result => {
                console.log(result)
                this.getAllExpressions()
            })
            .catch(error => {
                console.error(error)
            })
        },

        // DESTINATAIRES
        getAllDestinataires(){
            api.get(`/get-detinataires`)
            .then(result => {
                console.log("Destinataires réccuperées avec succès")
                this.destinataires = result.data.destinataires
            })
            .catch(error => {
                console.error(error)
            })
        },

        ajouterDestinataires(){
            let destinataire = document.querySelector('#nouveau-destinataire').value
            let data = {
                destinataire : destinataire
            }
            api.post(`/new-detinataires`, data)
            .then(result => {
                console.log(result)
                this.getAllDestinataires()
            })
            .catch(error => {
                console.error(error)
            })
        },

        supprimerDestinataires(id){
            api.delete(`/delete-destinataire/${id}`)
            .then(result => {
                console.log(result)
                this.getAllDestinataires()
            })
            .catch(error => {
                console.error(error)
            })
        },
        
        // CHAMPS OBLIGATOIRES DU FORMULAIRE
        getAllFormRequirements(){
            api.get(`/get-champs-obligatoires-status`)
            .then(result => {
                console.log(result)
                Object.assign(this.formRequirements, result.data.form_requirements)

            })
            .catch(error => {
                console.error(error)
            })
        },
        updateFormRequirements(key){
            console.log(key)
            api.put(`/update-champs-obligatoires-status/${key}`)
            .then(result => {
                console.log(result)
                this.getAllFormRequirements()
            })
            .catch(error => {
                console.error(error)
            })
        },
        // MODEL IA
        getSpamshieldModelInfos(){
            api.get(`/get-ai-model-infos`)
            .then(result => {
                console.log(result)
                this.modelInfos = result.data.spamshield_infos
            })
            .catch(error => {
                console.error(error)
            })
        },

        resetModel(){
            api.get(`/build_virgin_model`)
            .then(result => {
                console.log(result)
                this.getSpamshieldModelInfos()
            })
            .catch(error => {
                console.error(error)
            })
        
        },

        retrainModel(){
            if(this.modelInfos.training_data > 15){
                api.get("/retrain_model")
                .then(result => {
                    console.log(result)
                })
                .catch(error => {
                    console.error(error)
                })
            }
            else{
                alert("Pas assez de données pour réentraîner le modèle. Au moins 15 exemples sont nécessaires. Utilisez le banc de test pour ajouter des exemples ou attendez de nouveaux messages.")
            }
        }

    },
    mounted(){
        this.getAllExpressions()
        this.getAllDestinataires()
        this.getSpamshieldModelInfos()
        this.getAllFormRequirements()
        this.getSpamshieldModelInfos()
    }
}
 
</script>

<style scoped>
div.title{
    margin-top: 10px;
}

div.title h3{
    font-size: 16px;
}

main{
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
}
section{
    padding: 10px 20px;
    padding-bottom: 30px;
}

div.cards{
    display: grid;
    gap: 20px;
    margin-top: 20px;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    color: #65639B;

}
div.card{
    /* min-height: 200px; */
    background-color: #F7F8FC;
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


ul{
    list-style: none;
}

div.card ul li{
    opacity: 0.6;
    font-size: 16px;
}

div.card{
    padding: 20px;
}

div.card p {
    opacity: 0.6;
    font-size: 16px;
}

p.alert{
    color: rgb(253, 56, 56);
    margin-top: 10px;   
}

input[type="search"]{
    border:  #03005b5b 1px solid;
    border-radius: 5px;
    height: 25px;
    width: 100%;
}

fieldset{
    display: flex;
    gap: 10px;
    margin-top: 30px;
}

div.card div.liste_affichages div{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    /* margin-bottom: 30px; */
    background-color: #0301390a;
    border-radius: 10px;
    /* border-bottom: #03013947 1px solid; */
    padding: 10px;
}

div.card div.liste_affichages{
    max-height: 150px;
    overflow-y: scroll;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}



div.card div.liste_affichages button{
    color: white;
    background-color: #ff00006c;
}

/* CARD 1 */

div.card1{
    position: relative;
    padding-bottom: 50px;
}
div.card1 div.card1-lateral ul li:first-child{
    font-weight: 600;
    margin-bottom: 10px;
    text-decoration: underline;
}
div.card1 div.card1-lateral{
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    margin-bottom: 25px;
    
}

div.card1 ul strong{
    margin-left: 10px;
    opacity: 1!important;
    color: #030139;
}

div.card1 div.buttons{
    position: absolute;
    right: 20px;
    bottom: 20px;
    display: flex;
    gap: 10px;
}




/* CARD3 */
section.model-ia div.card3{
    position: relative;
}



section.model-ia div.card3 button{
    position: absolute;
    right: 20px;
    bottom: 20px;
}

/* destinataire et regex interdites */
section.expression-interdites .cards,
section.destinataires .cards {
    grid-template-columns: 1fr 2fr;
}

section.expression-interdites .card1,
section.destinataires .card1 {
    grid-column: 1 / 2;
}

section.expression-interdites .card2,
section.destinataires .card2 {
    grid-column: 2 / 3;
}

/* metadonnée */
section.metadonnee-formulaire div.card{
    position: relative;
    padding-right: 50px;
}

section.metadonnee-formulaire input[type="checkbox"]{
    position: absolute;
    right: 20px;
    bottom: 20px;
}
</style>