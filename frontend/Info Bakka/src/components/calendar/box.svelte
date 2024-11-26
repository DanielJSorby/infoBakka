<script>
	import Box from './box.svelte';
    export let time = '12:15-13:15';
    export let fag = 'fag';
    export let color = '#FF5252'
</script>

<div class="box" style="background-color: {color};">
    <div class="time-container">
        <p>{time}</p>
    </div>
    <div class="fag-container">
        <h2>{fag}</h2>
    </div>
</div>

<style>
    .box {
        width: 100%;
    }
</style>