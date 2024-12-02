<script lang="ts">
    import { onMount } from 'svelte';

    let weather = 'clearsky_day';
    let temperature = '0';
    let weatherData: any = null;

    const d = new Date();
    const dayList = ['Søndag', 'Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag'];
    const day = dayList[d.getDay()];
    const date = d.getDate();
    const monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Des'];
    const month = monthList[d.getMonth()];

    async function fetchWeatherData() {
        try {
            const response = await fetch('http://localhost:8000/weather');
            const reader = response.body?.getReader();
            if (!reader) return;

            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const text = new TextDecoder().decode(value);
                const chunks = text.split('\n\n');
                
                for (const chunk of chunks) {
                    if (chunk.trim()) {
                        try {
                            const data = JSON.parse(chunk);
                            if (data && data[0]) {  // Check if we have data
                                weatherData = data[0];  // Get first forecast (current)
                                weather = weatherData.symbol_code || 'clearsky_day';
                                temperature = Math.round(weatherData.details.air_temperature).toString();
                            }
                        } catch (parseError) {
                            console.error('Error parsing weather data:', parseError);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error fetching weather data:', error);
        }
    }

    onMount(() => {
        fetchWeatherData();
    });
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
