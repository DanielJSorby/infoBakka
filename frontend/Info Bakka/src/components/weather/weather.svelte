<script>
    export let weather = 'overskyet';
    export let temperature = '17';

    const d = new Date();
    const dayList = ['Søndag', 'Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag'];
    const day = dayList[d.getDay()];
    const date = d.getDate();
    const monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'];
    const month = monthList[d.getMonth()];

</script>

<div class="body {weather}" style="background-image: url(https://raw.githubusercontent.com/metno/weathericons/89e3173756248b4696b9b10677b66c4ef435db53/weather/svg/{weather}.svg);">
    <h2 class="semi-bold temperature">{temperature}°C</h2>
    <p class="thin date">{day} {date}. {month}</p>
</div>

<style>

    .body {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 360px;
        width: 100%;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        color: #707070;
        text-shadow: 2px 2px 2px rgba(255,255,255,0.4);
    }

    .temperature {
        font-size: 64px;
    }

    .date {
        font-size: 32px;
    }
</style>
