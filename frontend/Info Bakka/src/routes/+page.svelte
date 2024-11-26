<script>
    import CalendarBox from '../components/calendar/box.svelte'
    import Weather from '../components/weather/weather.svelte'
</script>

<Weather weather='overskyet' temperature='17' day='Onsdag' date='25' month='Nov'/>

<div class="calendar">
    <h3 class="regular">Onsdag</h3>
    <div class="line">Hei</div>
    <CalendarBox fag='Norsk' time='08:15-09:45'/>
    <div class="line">Hei</div>
    <CalendarBox fag='Matte' time='10:00-11:30' color='#81C784'/>
</div>

<style>
    .calendar {
        width: 404px;
        height: 276px;
        overflow: hidden;
        background-color: #fff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border-radius: 32px;
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
</style>