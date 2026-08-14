<template>
<section class="login-and-deco">
    <div class="deco">
        <div class="step">
            <h2>Étape 1 : Recevoir votre code de connexion</h2>
            <p>Saisissez votre adresse e-mail afin de recevoir un code de connexion à usage unique.</p>
        </div>
        <div class="step">
            <h2>Étape 2 : Valider votre connexion</h2>
            <p>Entrez le code de connexion à usage unique reçu par e-mail pour accéder à l'application.</p>
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
                        <input type="email" v-model="connexionForm.email" :disabled="emailDisabled">
                    </fieldset>
                    <button v-on:click="envoyerCode">Recevoir</button>
                </div>
            </div>


            <div class="step2" v-if="codeEnvoye">
                <div class="code">
                    <fieldset>
                        <label>Code de connexion</label>
                        <input type="text" v-model="connexionForm.code">
                    </fieldset>
                    <button v-on:click="verifierCode">Valider</button>
                </div>
            </div>
    </form>
</section>
</template>
<script>
import api from '@/axios/axios';

export default{
    data(){
        return{
            connexionForm:{
                email: '',
                code:'',
                
            },
            codeEnvoye: false
        }
    },
    methods:{
        envoyerCode(){
            this.codeEnvoye = true
            const data = {
                email:this.connexionForm.email
            }
            api.post('/envoyerCode', data)
            .then(response =>{
            })
            .catch(error => {
                console.error(error)
            })
        },

        verifierCode(){
            this.$router.push('/tableau-de-bord')
            const data = {
                code: this.connexionForm.code
            }
            api.post('/envoyerCode', data)
            .then(response =>{
                this.$router.push('/tableau-de-bord')
            })
            .catch(error => {
                console.error(error)
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
    padding: 40px 30px ;
}

div.deco p, div.deco h2{
    color: white;
}

form{
    padding: 40px 60px ;
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

div.email,div.code{
    display: flex;
    gap: 15px;
    align-items: flex-start;
}

input{
    width: 300px;
    height: 25px;
    margin-top: 5px;
}

div.code input {
    width: 200px;
}

button{
    position: relative;
    bottom: -22px;
}
</style>