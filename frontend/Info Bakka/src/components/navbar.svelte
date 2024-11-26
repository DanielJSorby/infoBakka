<script>
    export let page = 'home'
</script>

<div class="nav">
    <a href="/"><img src="/src/images/navbar/home.svg" alt=""></a>
    <a href="/weather"><img src="/src/images/navbar/weather.svg" alt=""></a>
    <a href="/calendar"><img src="/src/images/navbar/calendar.svg" alt=""></a>
    <a href="/ruter"><img src="/src/images/navbar/ruter.svg" alt=""></a>
</div>

<style>
    .nav {
        background-color: #00b9d5cd;
        border-radius: 26px;
        width: 240px;
        height: 52px;
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        justify-content: space-around;
        z-index: 1000; /* Sørger for at navbaren er øverst */
    }
</style>