<script>
    export let time = '12:15-13:15';
    export let fag = 'fag';
    export let color = '#FF5252'
</script>

<div class="box" style="background-color: {color};">
    <div class="time-container">
        <p class="regular">{time}</p>
    </div>
    <div class="fag-container">
        <h2 class="bold">{fag}</h2>
    </div>
</div>

<style>
    .box {
        width: 374px;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        border-radius: 20px;
    }

    .time-container {
        position: absolute;
        top: 5px;
        left: 5px;
        font-size: 16px;
        color: #E0E0E0;
    }

    .fag-container {
        font-size: 36px;
        color: #FFFFFF;
    }
</style>