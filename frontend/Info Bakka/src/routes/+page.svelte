<script lang="ts">
    import Navbar from '../components/navbar.svelte';
    import CalendarBox from '../components/calendar/box.svelte';
    import Weather from '../components/weather/weather.svelte';
    import Ruter from '../components/ruter/ruter.svelte';
    import timeplanData from '../data/timeplan.json';

    interface Block {
        fag: string;
        farge: string;
        startTid: string;
        sluttTid: string;
    }

    interface DayPlan {
        imit2?: Record<string, Block>;
        imstit2?: Record<string, Block>;
    }

    const timeplan: Record<string, DayPlan> = timeplanData;

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
        let blocks = timeplan[dayName]?.imstit2;

        if (!blocks) return { blocks: [], dayName };

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

        if (nextBlocks.length === 0) {
            // Hvis det ikke er flere blokker for dagen, sjekk neste dag
            let nextDay = (day + 1) % 7;
            let nextDayName = getDayName(nextDay);
            blocks = timeplan[nextDayName]?.imstit2;

            if (blocks) {
                for (const block in blocks) {
                    nextBlocks.push(blocks[block]);
                }
            }

            return { blocks: nextBlocks.slice(0, 2), dayName: nextDayName };
        }

        return { blocks: nextBlocks.slice(0, 2), dayName };
    }

    let { blocks: currentAndNextBlocks, dayName: displayDayName } = getCurrentAndNextBlocks(dayName);
</script>

<Navbar />

<Weather weather='rain' temperature='17' day='Onsdag' date='25' month='Nov'/>

<h1 class="header bold">Info-Bakka</h1>

<a href="/calendar" class="calendar-link">
    <div class="calendar">
        <h3 class="regular">{displayDayName[0].toUpperCase() + displayDayName.slice(1)}</h3>
        <div class="line">Hei</div>
        {#if currentAndNextBlocks.length > 0}
            {#each currentAndNextBlocks as block}
                <CalendarBox fag={block.fag[0].toUpperCase() + block.fag.slice(1)} time={`${block.startTid}-${block.sluttTid}`} color={block.farge}/>
                <div class="line">Hei</div>
            {/each}
        {:else}
            <div>Ingen blokk akkurat nå</div>
        {/if}
    </div>
</a>

<Ruter amount={6}/>

<p>&copy; InfoBakka</p>
<p>&copy; InfoBakka</p>
<p>&copy; InfoBakka</p>
<p>&copy; InfoBakka</p>

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