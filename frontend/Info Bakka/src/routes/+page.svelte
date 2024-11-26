<script lang="ts">
    import Navbar from '../components/navbar.svelte';
    import Weather from '../components/weather/weather.svelte';
    import Ruter from '../components/ruter/ruter.svelte';
    import Calendar from '../components/calendar/calendar.svelte';
</script>

<Navbar />

<Weather weather='rain'/>

<h1 class="header bold">Info-Bakka</h1>

<Calendar />

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
</style>