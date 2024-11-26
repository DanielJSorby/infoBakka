<script lang="ts">
    import Navbar from '../components/navbar.svelte';
    import CalendarBox from '../components/calendar/box.svelte';
    import Weather from '../components/weather/weather.svelte';
    import Rute from '../components/ruter/rute.svelte';
    import timeplan from '../data/timeplan.json';

    let time = new Date();
    let day = time.getDay();

    // Funksjon for å få navnet på dagen
    function getDayName(day: number) {
        const days = ['søndag', 'mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag'];
        return days[day];
    }

    let dayName = getDayName(day);

    // Funksjon for å konvertere tid fra HH:MM til minutter siden midnatt
    function timeToMinutes(time: string) {
        const [hours, minutes] = time.split(':').map(Number);
        return hours * 60 + minutes;
    }

    // Funksjon for å sjekke de nåværende og neste blokkene basert på nåværende tid
    function getCurrentAndNextBlocks(dayName: string) {
        const now = new Date();
        const currentMinutes = now.getHours() * 60 + now.getMinutes();
        const blocks = timeplan[dayName]?.imstit2;

        if (!blocks) return [];

        let currentBlock = null;
        let nextBlocks = [];

        for (const block in blocks) {
            const startMinutes = timeToMinutes(blocks[block].startTid);
            const endMinutes = timeToMinutes(blocks[block].sluttTid);
            if (currentMinutes >= startMinutes && currentMinutes <= endMinutes) {
                currentBlock = blocks[block];
            } else if (currentMinutes < startMinutes) {
                nextBlocks.push(blocks[block]);
            }
        }

        if (currentBlock) {
            nextBlocks.unshift(currentBlock);
        }

        return nextBlocks.slice(0, 2);
    }

    let currentAndNextBlocks = getCurrentAndNextBlocks(dayName);
</script>

<Navbar />

<Weather weather='rain' temperature='17' day='Onsdag' date='25' month='Nov'/>

<h1 class="header bold">Info-Bakka</h1>

<a href="/calendar" class="calendar-link">
    <div class="calendar">
        <h3 class="regular">{dayName}</h3>
        <div class="line">Hei</div>
        {#if currentAndNextBlocks.length > 0}
            {#each currentAndNextBlocks as block}
                <CalendarBox fag={block.fag} time={`${block.startTid}-${block.sluttTid}`} color={block.farge}/>
                <div class="line">Hei</div>
            {/each}
        {:else}
            <div>Ingen blokk akkurat nå</div>
        {/if}
    </div>
</a>

<Rute type='buss' navn='Kjelsås Stasjon' planlagtTid=3 faktiskTid=5 linje=54/>
<Rute type='trikk' navn='Sinsen via Grefsen' planlagtTid=7 faktiskTid=7 linje=18/>

<p>© InfoBakka</p>
<p>© InfoBakka</p>
<p>© InfoBakka</p>
<p>© InfoBakka</p>
<p>© InfoBakka</p>

<style>
    .header {
        color: white;
        font-size: 64px;
        text-align: center;
    }
    .calendar {
        width: 98%;
        height: 276px;
        overflow: hidden;
        background-color: #fff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border-radius: 32px;
        margin: 0 auto;
    }

    .calendar h3 {
        color: #707070;
        align-self: flex-start;
        margin-left: 32px;
        font-size: 28px;
    }

    .calendar .line {
        width: 354px;
    }

    .calendar-link {
        text-decoration: none; /* Fjerner blå understrek */
    }
</style>