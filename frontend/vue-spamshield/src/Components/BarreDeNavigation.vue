<template>
<header>
    <h1 class="logo-title">Spam Shield</h1>
    <nav class="nav-bar">
        <ul>
            <RouterLink to="/tableau-de-bord"><li>Tableau de bord</li></RouterLink>
            <RouterLink to="/banc-de-tests"><li>Banc de tests</li></RouterLink>
            <RouterLink to="/parametres"><li>Paramètres</li></RouterLink>
            <RouterLink to="/">
                <li>
                    <svg xmlns="http://www.w3.org/2000/svg" width=" 25" height="20" fill="currentColor" class="bi bi-box-arrow-in-right" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M6 3.5a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-2a.5.5 0 0 0-1 0v2A1.5 1.5 0 0 0 6.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-8A1.5 1.5 0 0 0 5 3.5v2a.5.5 0 0 0 1 0z"/>
                        <path fill-rule="evenodd" d="M11.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5H1.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/>
                    </svg>
                </li>
            </RouterLink>
        </ul>
    </nav>
</header>
</template>

<script>
</script>

<style scoped>
header{
    background-color: white;
    border-bottom: #282f7f36 1px solid;
}

header h1{
    font-family: "Major Mono Display", monospace;
    font-size: 20PX;
}

header{
    display: flex;
    justify-content: space-between;
    padding: 10px 20px;
    padding-bottom: 18px;
    padding-top: 15px;
    margin-bottom: 50px;
}
header nav.nav-bar ul{
    display: flex;
    list-style-type: none;
    gap: 40px;
    font-size: 16px;
    position: relative;
    bottom: -5px;
}

header nav.nav-bar ul li{
    cursor: pointer;
}


</style>