<template>
<section class="login-and-deco">
    <div class="deco">
        <div class="step">
            <h2>Étape 1 : Recevoir votre code de connexion</h2>
            <p>Saisissez votre adresse e-mail afin de recevoir un code de connexion à usage unique.</p>
        </div>

        <div class="step">
            <h2>Étape 2 : Valider votre connexion</h2>
            <p>Entrez le code reçu par e-mail pour accéder à l'application.</p>
        </div>

        <div class="step">
            <h2>Note :</h2>
            <p>Aucun e-mail reçu ? Vérifiez vos spams et vos droits administrateur.</p>
        </div>
    </div>

    <form @submit.prevent>
        <div class="step1" v-if="!codeEnvoye">
            <div class="email">
                <fieldset>
                    <label>Adresse e-mail</label>
                    <input
                        type="email"
                        v-model="connexionForm.email"
                        required
                    >
                </fieldset>

                <button
                    type="button"
                    @click="envoyerCode"
                >
                    Recevoir
                </button>
            </div>
        </div>

        <div class="step2" v-if="codeEnvoye">
            <div class="code">
                <fieldset>
                    <label>Code de connexion</label>
                    <input
                        type="text"
                        v-model="connexionForm.code"
                        required
                    >
                </fieldset>

                <button
                    type="button"
                    @click="verifierCode"
                >
                    Valider
                </button>
            </div>
        </div>

        <p v-if="erreur">
            {{ erreur }}
        </p>
    </form>
</section>
</template>

<script>
import api from '@/axios/axios';

export default {
    data() {
        return {
            connexionForm: {
                email: '',
                code: ''
            },
            codeEnvoye: false,
            erreur: ''
        }
    },

    methods: {
        envoyerCode() {
            this.erreur = ''

            api.post('/auth/request-code', {
                email: this.connexionForm.email
            })
            .then(() => {
                this.codeEnvoye = true
            })
            .catch(error => {
                this.erreur =
                    error.response?.data?.detail
                    || "Impossible d'envoyer le code."
            })
        },

        verifierCode() {
            this.erreur = ''

            api.post('/auth/verify-code', {
                email: this.connexionForm.email,
                code: this.connexionForm.code
            })
            .then(async response => {
                console.log("verify-code :", response.data)

                const auth = await api.get('/auth/me')

                console.log("auth/me :", auth.data)

                this.$router.push('/tableau-de-bord')
            })
            .catch(error => {
                console.error(
                    "Erreur auth :",
                    error.response?.status,
                    error.response?.data
                )

                this.erreur =
                    error.response?.data?.detail
                    || "Code invalide."
            })
        }
    }
}
</script>

<style scoped>
section.login-and-deco{
    display: flex;
    margin-top: 100px;
    justify-self: center;
}

div.deco{
    background-color: #4D5AF7;
    display: inline-block;
    padding: 40px 30px;
}

div.deco p,
div.deco h2{
    color: white;
}

form{
    padding: 40px 60px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 530px;
    background-color: white;
}

p{
    margin-top: 5px;
    margin-bottom: 30px;
    font-size: 14px;
}

fieldset{
    display: flex;
    flex-direction: column;
}

div.email,
div.code{
    display: flex;
    gap: 15px;
    align-items: flex-start;
}

input{
    width: 300px;
    height: 25px;
    margin-top: 5px;
}

div.code input{
    width: 200px;
}

button{
    position: relative;
    bottom: -22px;
}
</style>