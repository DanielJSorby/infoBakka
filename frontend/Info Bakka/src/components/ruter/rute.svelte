<script lang="ts">
    export let type: string;
    export let navn: string;
    export let planlagtTid: string;
    export let faktiskTid: string;
    export let linje: number;
</script>

<div class="rute">
    <div class="linje-navn">
    <div class="linje {type}">
            {#if type === 'buss'}
                <svg id="Bus_Circle_1" data-name="Bus Circle 1" xmlns="http://www.w3.org/2000/svg" width="12.742" height="12.742" viewBox="0 0 12.742 12.742">
                <path id="Path_15" data-name="Path 15" d="M11.156,19.528a.728.728,0,1,1-.728-.728.748.748,0,0,1,.728.728Z" transform="translate(-6.196 -11.155)" fill="#fff"/>
                <path id="Path_16" data-name="Path 16" d="M14.911,11.2H6.082a.2.2,0,0,0-.182.182v3.686a.2.2,0,0,0,.182.182H7.174a1.133,1.133,0,0,1,1.274-1,1.115,1.115,0,0,1,1,1h2a1.133,1.133,0,0,1,1.274-1,1.115,1.115,0,0,1,1,1H14.82A.2.2,0,0,0,15,15.068V11.382C15.093,11.291,15,11.2,14.911,11.2ZM8.175,13.475H6.355V11.928h1.82Zm2.139,0H8.494V11.928h1.82Zm2.184,0h-1.82V11.928H12.5Zm2.184,0h-1.82V11.928h1.82Z" transform="translate(-4.125 -7.013)" fill="#fff"/>
                <path id="Path_17" data-name="Path 17" d="M20.556,19.528a.728.728,0,1,1-.728-.728.748.748,0,0,1,.728.728Z" transform="translate(-11.318 -11.155)" fill="#fff"/>
                <path id="Path_18" data-name="Path 18" d="M8.371,2.455A5.916,5.916,0,1,1,2.455,8.371,5.9,5.9,0,0,1,8.371,2.455m0-.455a6.371,6.371,0,1,0,6.371,6.371A6.39,6.39,0,0,0,8.371,2Z" transform="translate(-2 -2)" fill="#fff"/>
                </svg>
            {:else if type === 'trikk'}
                <svg xmlns="http://www.w3.org/2000/svg" width="12.754" height="12.754" viewBox="0 0 12.754 12.754">
                <g id="Tram_Circle" data-name="Tram Circle" transform="translate(-2 -2)">
                    <rect id="Rectangle_45" data-name="Rectangle 45" width="8.199" height="0.638" transform="translate(4.278 10.791)" fill="#fff"/>
                    <path id="Path_19" data-name="Path 19" d="M15.135,11.31l-.182-.774-.319-1.367h0l-.046-.182c-.046-.091-.091-.137-.182-.137H10.626l.82-.774a.22.22,0,0,0,0-.319L11.4,7.711,10.261,6.8H9.624L10.99,7.893l-1,.865H6.708c-.091,0-.182.046-.182.137l-.182.774L5.98,11.218v.091a.938.938,0,0,0,.137.683l.319.5H7.574v.228a.311.311,0,0,0,.319.319h1a.311.311,0,0,0,.319-.319v-.228h2.642v.228a.311.311,0,0,0,.319.319h1a.311.311,0,0,0,.319-.319v-.228h1.139l.364-.5A.858.858,0,0,0,15.135,11.31Zm-6.878-.182H6.435l.319-1.5h1.5Zm2.141,0H8.576v-1.5H10.4Zm2.1,0H10.671v-1.5h1.822Zm.364,0v-1.5h1.5l.319,1.5Z" transform="translate(-2.158 -2.614)" fill="#fff"/>
                    <path id="Path_20" data-name="Path 20" d="M8.377,2.456A5.922,5.922,0,1,1,2.456,8.377,5.91,5.91,0,0,1,8.377,2.456m0-.456a6.377,6.377,0,1,0,6.377,6.377A6.4,6.4,0,0,0,8.377,2Z" fill="#fff"/>
                </g>
                </svg>
            {/if}
            <p class="semi-bold">{linje}</p>
        </div>
        {navn}
    </div>
    <div class="tid">
        {#if planlagtTid === faktiskTid}
            <p>{faktiskTid}{faktiskTid !== 'Nå' ? ' min' : ''}</p>
        {:else}
            <p class="forsinket">{planlagtTid}{planlagtTid !== 'nå' ? ' min' : ''}</p>
            <p>{faktiskTid}{faktiskTid !== 'Nå' ? ' min' : ''}</p>
        {/if}
    </div>
</div>

<style>
    .rute .linje-navn .linje.buss {
        background-color: #FF5252;
    }
    .rute .linje-navn .linje.trikk{
        background-color: #00B8D5;
    }

    .rute .linje-navn .linje {
        border-radius: 26px;
        width: fit-content;
        padding: 2px 8px;
        display: flex;
        align-items: center;
        justify-content: space-around;
    }
    
    .rute {
        color: white;
        width: 100%;
        display: flex;
        justify-content: space-between;
    }

    .rute * {
        display: flex;
        gap: 4px;
    }

    .forsinket {
        color: #FFD900;
        text-decoration: line-through;
    }
</style>