<script>
    export let weather = 'overskyet';
    export let temperature = '17';
    export let day = 'Onsdag'
    export let date = '25'
    export let month = 'Nov'

</script>

<div class="body {weather}">
    <h2 class="semi-bold temperature">{temperature}</h2>
    <p class="thin date">{day} {date}. {month}</p>
</div>

<style>
    .overskyet {
        background-image: url(/src/images/weather/overskyet.svg);
    }

    .skyet {
        background-image: url(/src/images/weather/skyet.svg);
    }

    .sol {
        background-image: url(/src/images/weather/sol.svg);
    }

    .regn {
        background-image: url(/src/images/weather/regn.svg);
    }

    .body {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 260px;
        width: 100%;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        color: #707070;
    }

    .temperature {
        font-size: 64px;
        padding-right: 100px;
    }

    .date {
        font-size: 32px;
    }
</style>
