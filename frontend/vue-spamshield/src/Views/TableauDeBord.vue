<template>


<!-- BODY -->
<main>
    <!-- PERIOD -->
    <div class="period-and-date">
        <h2 class="period">01/07/2026 - 07/07/2026</h2>
    </div>
    <!-- DASHBORD SECTION -->
    <section class="dashbord">
        <div class="global-infos-cards">
            <!-- INFO CARD 1 -->
            <div class="g-info-card card-deco">
                <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                        <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414zM0 4.697v7.104l5.803-3.558zM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586zm3.436-.586L16 11.801V4.697z"/>
                    </svg>
                    <h3>Messages</h3>
                </div>
                <p class="info-value">17</p>
            </div>
            <!-- INFO CARD 2 -->
            <div class="g-info-card card-deco">
                <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check2-all" viewBox="0 0 16 16">
                        <path d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0"/>
                        <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708"/>
                    </svg>
                    <h3>Légitimes</h3>
                </div>
                <p class="info-value">12</p>
            </div>
            <!-- INFO CARD 3 -->
            <div class="g-info-card card-deco">
                <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                        <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                    </svg>
                    <h3>Indésirables</h3>
                </div>
                <p class="info-value">5</p>
            </div>
            <!-- INFO CARD 4 -->
            <div class="g-info-card g-info-card-blue card-deco">
                <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-pen-fill" viewBox="0 0 16 16">
                        <path d="m13.498.795.149-.149a1.207 1.207 0 1 1 1.707 1.708l-.149.148a1.5 1.5 0 0 1-.059 2.059L4.854 14.854a.5.5 0 0 1-.233.131l-4 1a.5.5 0 0 1-.606-.606l1-4a.5.5 0 0 1 .131-.232l9.642-9.642a.5.5 0 0 0-.642.056L6.854 4.854a.5.5 0 1 1-.708-.708L9.44.854A1.5 1.5 0 0 1 11.5.796a1.5 1.5 0 0 1 1.998-.001"/>
                    </svg>
                    <h3>Corrections</h3>
                </div>
                <p class="info-value">1</p>
            </div>
            <!-- INFO CARD 5 -->
            <div class="g-info-card  g-info-card-blue card-deco">
                <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" class="bi bi-gear-wide-connected" viewBox="0 0 16 16">
                        <path d="M7.068.727c.243-.97 1.62-.97 1.864 0l.071.286a.96.96 0 0 0 1.622.434l.205-.211c.695-.719 1.888-.03 1.613.931l-.08.284a.96.96 0 0 0 1.187 1.187l.283-.081c.96-.275 1.65.918.931 1.613l-.211.205a.96.96 0 0 0 .434 1.622l.286.071c.97.243.97 1.62 0 1.864l-.286.071a.96.96 0 0 0-.434 1.622l.211.205c.719.695.03 1.888-.931 1.613l-.284-.08a.96.96 0 0 0-1.187 1.187l.081.283c.275.96-.918 1.65-1.613.931l-.205-.211a.96.96 0 0 0-1.622.434l-.071.286c-.243.97-1.62.97-1.864 0l-.071-.286a.96.96 0 0 0-1.622-.434l-.205.211c-.695.719-1.888.03-1.613-.931l.08-.284a.96.96 0 0 0-1.186-1.187l-.284.081c-.96.275-1.65-.918-.931-1.613l.211-.205a.96.96 0 0 0-.434-1.622l-.286-.071c-.97-.243-.97-1.62 0-1.864l.286-.071a.96.96 0 0 0 .434-1.622l-.211-.205c-.719-.695-.03-1.888.931-1.613l.284.08a.96.96 0 0 0 1.187-1.186l-.081-.284c-.275-.96.918-1.65 1.613-.931l.205.211a.96.96 0 0 0 1.622-.434zM12.973 8.5H8.25l-2.834 3.779A4.998 4.998 0 0 0 12.973 8.5m0-1a4.998 4.998 0 0 0-7.557-3.779l2.834 3.78zM5.048 3.967l-.087.065zm-.431.355A4.98 4.98 0 0 0 3.002 8c0 1.455.622 2.765 1.615 3.678L7.375 8zm.344 7.646.087.065z"/>
                    </svg>
                    <h3>Reclassements</h3>
                </div>
                <p class="info-value">2</p>
            </div>
        </div>
        <div class="global-infos-graphs">
            <!-- INFO GRAPH 1 -->
            <div class="g-info-graph g-info-graph-dis card-deco">
                <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                        <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414zM0 4.697v7.104l5.803-3.558zM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586zm3.436-.586L16 11.801V4.697z"/>
                    </svg>
                    <h3>Distribution par Catégories</h3>
                </div>
                <GraphDistributionParCat></GraphDistributionParCat>

            </div>
            <!-- INFO GRAPH 2 -->
            <div class="g-info-graph g-info-graph-evo card-deco">
                <div class="title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                        <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414zM0 4.697v7.104l5.803-3.558zM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586zm3.436-.586L16 11.801V4.697z"/>
                    </svg>
                    <h3>Evolution par Catégories</h3>
                </div>
                <GraphEvolutionParGraph></GraphEvolutionParGraph>
            </div>
        </div>
    </section>
    <!-- RECEPTION SECTION -->
    <section class="boite-de-reception">
        <div class="messages-and-filters">
            <!-- FILTERS -->
            <div class="filters">
                <!-- TRIER PAR -->
                <fieldset class="trier-par">
                    <label for="trier">Trier par : </label>
                    <select name="trier" id="trier-par">
                        <option value="None"></option>
                        <option value="plus-recents">plus récents</option>
                        <option value="moins-recents">moins récents</option>
                    </select>
                </fieldset>
                <!-- FILTRER PAR -->
                <fieldset class="filtrer-par">
                    <label for="filtrer">Filtrer par : </label>
                    <select name="filtrer" id="filtrer-par">
                        <option value="None"></option>
                        <option value="legitimes">légitimes</option>
                        <option value="indésirables">indésirables</option>
                        <option value="consultés">consultés</option>
                        <option value="non-consultés">non consultés</option>
                        <option value="corrigés">corrigés</option>
                        <option value="non-corrigés">non corrigés</option>
                        <option value="reclassés">reclassés</option>
                        <option value="non-reclassés">non reclassés</option>
                    </select>
                </fieldset>
            </div>
            <!-- MESSAGES -->
            <div class="messages">
                <!-- SELECTED MESSAGE -->
                <div class="card selected-card  card-deco">
                    <h3>
                        <svg style="position: relative; top: 2px;" xmlns="http://www.w3.org/2000/svg" width="14" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                        </svg>

                        Indésirable
                    </h3>
                    <span class="date">23/06/2026 13:30</span>
                    <p class="mail">j*******@o******.net</p>
                    <p class="message-resume">Lorem ipsum, du texte et encore du contenue et plus et enco, orem ipsum, du texte et encore du contenue et plus et enco...</p>
                </div>
                <!-- OTHER MESSAGES -->
                <div class="card card-deco">
                    <h3>
                        <svg style="position: relative; top: 2px;" xmlns="http://www.w3.org/2000/svg" width="14" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                        </svg>

                        Indésirable
                    </h3>
                    <span class="date">23/06/2026 13:30</span>
                    <p class="mail">j*******@o******.net</p>
                    <p class="message-resume">Lorem ipsum, du texte et encore du contenue et plus et enco, orem ipsum, du texte et encore du contenue et plus et enco...</p>
                </div>
                <div class="card card-deco">
                    <h3>
                        <svg style="position: relative; top: 2px;" xmlns="http://www.w3.org/2000/svg" width="14" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                        </svg>

                        Indésirable
                    </h3>
                    <span class="date">23/06/2026 13:30</span>
                    <p class="mail">j*******@o******.net</p>
                    <p class="message-resume">Lorem ipsum, du texte et encore du contenue et plus et enco, orem ipsum, du texte et encore du contenue et plus et enco...</p>
                </div>
                <div class="card card-deco">
                    <h3>
                        <svg style="position: relative; top: 2px;" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check2-all" viewBox="0 0 16 16">
                            <path d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0"/>
                            <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708"/>
                        </svg>

                        Légitime
                    </h3>
                    <span class="date">23/06/2026 13:30</span>
                    <p class="mail">j*******@o******.net</p>
                    <p class="message-resume">Lorem ipsum, du texte et encore du contenue et plus et enco, orem ipsum, du texte et encore du contenue et plus et enco...</p>
                </div>
                <div class="card card-deco">
                    <h3>
                        <svg style="position: relative; top: 2px;" xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/>
                        </svg>

                        Indésirable
                    </h3>
                    <span class="date">23/06/2026 13:30</span>
                    <p class="mail">j*******@o******.net</p>
                    <p class="message-resume">Lorem ipsum, du texte et encore du contenue et plus et enco, orem ipsum, du texte et encore du contenue et plus et enco...</p>
                </div>
            </div>
            
        </div>
        <div class="message-et-info">
            <!-- STATUS -->
            <div class="status">
                <!-- A ETE CONSULTE -->
                <div class="msg-consulte">
                    <p>Message consulté</p>
                    <input type="checkbox" checked disabled>
                </div>
                <!-- A ETE RECU PAR MAIL -->
                <div class="msg-consulte">
                    <p>Message reçu</p>
                    <input type="checkbox"  disabled>
                </div>
            </div>
            
            <div class="table-et-message">
                <!-- TABLE -->
                <div class="table-metrics">
                    <table class="card-deco">

                        <!-- LABEL FINAL -->
                        <tr class="label-final">
                            <th class="metrics-head">
                                Label Final
                            </th>
                            <td colspan="2" style="color: rgb(253, 56, 56); font-weight: 800;">
                                Indésirable
                            </td>
                        </tr>

                        <!-- MODEL IA -->
                        <tr class="model-ia">
                            <th class="metrics-head" rowspan="2">
                                Model IA
                            </th>
                            <th class="metrics-head-2">
                                Prédiction
                            </th>
                            <td>
                                Indésirable
                            </td>
                        </tr>
                        <tr class="model-ia">
                            <th class="metrics-head-2">
                                Score de confiance
                            </th>
                            <td>
                                0.92
                            </td>
                        </tr>

                        <!-- REGLES METIERS -->
                        <tr class="regle-metiers">
                            <th class="metrics-head" rowspan="2">
                                Règles Métiers
                            </th>
                            <th class="metrics-head-2">
                                Délibération
                            </th>
                            <td>
                                Indésirable
                            </td>
                        </tr>
                        <tr class="regle-metiers">
                            <th class="metrics-head-2">
                                Shémas interdits retrouvés
                            </th>
                            <td>
                                <ul>
                                    <li>contient gibberish/charabia</li>
                                    <li>Aucun mail renseigné</li>
                                </ul>
                            </td>
                        </tr>

                        <!-- REVISONS -->
                        <tr class="revisons">
                            <th class="metrics-head" rowspan="2">
                                Révisons
                            </th>
                            <th class="metrics-head-2">
                                Reclassé
                            </th>
                            <td>
                                NON
                            </td>
                        </tr>
                        <tr class="regle-metiers">
                            <th class="metrics-head-2">
                                Corrigé
                            </th>
                            <td>
                                NON
                            </td>
                        </tr>
                    </table>
                </div>

                <!-- MESSAGE -->
                <div class="message card-deco">
                    <div class="title-and-menu">
                        <div class="title">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                                <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414zM0 4.697v7.104l5.803-3.558zM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586zm3.436-.586L16 11.801V4.697z"/>
                            </svg>
                            <h3>Message</h3>
                        </div>
                        <div class="menu">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
                                <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3m5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3"/>
                            </svg>
                        </div>
                    </div>
                    <div class="content-and-metadata">
                        <p><strong>Date :</strong> 23/06/2026  -  13:30</p>
                        <p><strong>Nom :</strong> D**</p>
                        <p><strong>Prenom :</strong> J***</p>
                        <p><strong>Email :</strong> j******@*****.com</p>
                        <div class="content">
                            <strong>Message :</strong>
                            <p>Lorem ipsum dolor sit amet consectetur. Condimentum tellus nibh dis quis gravida non feugiat imperdiet fermentum. Lacus pulvinar facilisis mauris vitae in. Sed rhoncus ac etiam arcu quam quis eget. Libero et nisi dictum mattis metus in nunc ! </p>
                        </div>
                    </div>
                    <div class="correction">
                        <p>Ce message vous semble être légitime ?</p>
                        <button>Correction</button>
                    </div>
                </div>
            </div>
        </div>
    </section>
</main>
</template>

<script>
// COMPOSANTS GRAPHIQUES PLOTLY
import GraphDistributionParCat from '@/Components/GraphDistributionParCat.vue';
import GraphEvolutionParGraph from '@/Components/GraphEvolutionParGraph.vue';

export default{
    data(){
        return{

        }
    },
    components:{
        GraphDistributionParCat,
        GraphEvolutionParGraph,

    }
}

</script>

<style scoped>
h2.period{
    font-size: 16px;
    font-weight: 500;
}

/* INFO CARDS */
div.global-infos-cards{
    display: flex;
    gap:10px;
    margin-top: 20px;
    margin-bottom: 10px;
}

div.g-info-card{
    width: 220px;
    padding: 10px 20px;
}


div.g-info-card p.info-value{
    color: #6A70C7;
    font-size: 16px;
}


div.g-info-card-blue p.info-value{
    color: #ffffffb6;
}

div.g-info-card-blue h3{
    color: #ffffff;
    font-size: 14px;
}
div.g-info-card h3{
    font-size: 14px;
}

div.g-info-card-blue svg{
    color: #ffffff;
}

div.g-info-card-blue{
    background-color: #4D5AF7;
}

/* INFO GRAPHS */

div.global-infos-graphs{
    display: flex;
    gap:10px;
}

div.g-info-graph{
    height: 340px;
    padding: 10px 20px;
}
div.g-info-graph h3{
    font-size: 14px;
}
div.g-info-graph-dis{
    width: 40%;
}

div.g-info-graph-evo{
    width: 60%;
}

div#dis-per-cat,#evo-per-cat{
    width: 100%;
    height: 270px;
    border: 1px solid #b0ccfd81;
    border-radius: 10px;
    overflow: hidden;
}



/* BOITE DE RECEPTION */
section.boite-de-reception{
    display: flex;
    width: 100%;
    gap:20px;
    margin-top: 60px;
}
/* MESSAGES ET FILTERS */
div.messages-and-filters{
    width: 50%;
}
div.message-et-info{
    width: 50%;
}

/* FILTERS */
div.filters{
    display: flex;
    gap:20px;
    margin-left: 5px;
}
div.filters label{
    font-size: 14px;
    font-weight: 800;
}

select{
    background-color: transparent;
    border: #282f7f7e 1px solid;
    width: 160px;
    height: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    padding-left: 10px;
}

/* MESSAGE CARD */

div.messages{
    display: flex;
    flex-direction: column;
    gap: 6px;
    height: 700px;
    overflow-y: scroll;
    padding-right: 12px;
    padding-bottom: 20px;
    padding-left: 5px;
}

div.messages div.card{
    width: 100%;
    padding: 10px 20px;
    padding-right: 30px;
    padding-bottom: 20px;
    position: relative;
    cursor: pointer;
}

div.messages div.card:hover{
    /* border: solid #6FB8F8 1.2px;  */

}

div.messages div.card h3{
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 10px;
}

div.messages div.card span.date{
    position: absolute;
    right: 20px;
    top: 10px;
    font-size: 14px;
    color: #5E5E5E;
}

div.messages div.card p{
    font-size: 16px;
}

div.messages div.card p.mail{
    font-size: 14px;
    color: #5E5E5E;
}
div.messages div.selected-card{

    position: relative;
}

div.messages div.selected-card::before{
    content: "";
    position: absolute;
    left: 0;
    width: 10px;
    height: 100%;
    background-color: #4d5af7; 
    top: 0;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}

/* STATUS */
div.status{
    display: flex;
    gap:30px;
    margin-bottom: 20px;
    margin-top: 30px;
}

div.status div{
    font-size: 14px;
    display: flex;
    gap: 10px;
    font-weight: 800;
}

div.table-et-message{
    display: flex;
    flex-direction: column;
    gap: 20px;
}
/* MESSAGE ZONE */

div.message{
    padding: 20px 25px;
    padding-bottom: 40px;
    position: relative;
}



div.message div.menu{
    position: absolute;
    top: 10px;
    right: 20px;
    cursor: pointer;
}

div.content-and-metadata{
    margin-top: 30px;
}

div.content-and-metadata p{
    font-size: 16px;
    line-height: 22px;
    color: #03005b9b;
}

div.content-and-metadata strong{
    font-weight: 800;
    font-size: 14px;
    margin-right: 5px;
    color: #03005B;
}

div.content-and-metadata div.content{
    margin-top: 15px;
    margin-bottom: 15px;
    padding-top: 20px;
    padding-bottom: 25px;
    border: #e3e8fc 1px solid;
    border-left: 0;
    border-right: 0; 
}

div.correction{
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding-top: 20px;
}

div.correction p{
    font-size: 16px;
    opacity: 0.6;
    padding-top: 5px;
}


/* TABLE */

div.table-metrics table{
    /* margin-top: 20px; */
    /* margin-bottom: 50px; */
    font-size: 14px;
    width:  100%;
    border-collapse : collapse;
    border-radius: 5px;
    overflow: hidden;
}

div.table-metrics table th{
    padding: 20px 20px;
    text-align: start;
    vertical-align: top;
    font-size: 14px;
}

div.table-metrics table th.metrics-head{
    background-color: #4d5af7;
    color: white;
    font-weight: 800;
    font-size: 14px;
    text-decoration: underline;
}

div.table-metrics table td{
    padding-left: 20px;
    text-align: start;
}

div.table-metrics table td ul{
    padding-top: 10px;
}

div.table-metrics table th,td{
    border-right: 1px solid #d0d9fc;
    border-bottom: 1px solid #d0d9fc;
}

th:last-child,td:last-child{
    border-right: none;
}
tr:last-child{
    border-bottom: none;
    border-radius: 10px;
}

tr td{
    /* font-weight: 800; */
    opacity: 0.6;
    font-size: 16px;
}



</style>