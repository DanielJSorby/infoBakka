<script lang="ts">
    import Rute from "./rute.svelte";
    export let amount: number = 10;

    interface RuteType {
        type: string;
        navn: string;
        planlagtTid: number;
        faktiskTid: number;
        linje: number;
        stopp: string;
    }

    let ruter: RuteType[] = [
        {
            "type": "buss",
            "navn": "Kjelsås Stasjon",
            "planlagtTid": 3,
            "faktiskTid": 5,
            "linje": 54,
            "stopp": "Jakobs kirke"
        },
        {
            "type": "trikk",
            "navn": "Sinsen via Grefsen",
            "planlagtTid": 7,
            "faktiskTid": 7,
            "linje": 18,
            "stopp": "Nybrua"
        },
        {
            "type": "buss",
            "navn": "Majorstuen",
            "planlagtTid": 5,
            "faktiskTid": 6,
            "linje": 20,
            "stopp": "Jakobs kirke"
        },
        {
            "type": "trikk",
            "navn": "Storo",
            "planlagtTid": 4,
            "faktiskTid": 4,
            "linje": 11,
            "stopp": "Nybrua"
        },
        {
            "type": "buss",
            "navn": "Tøyen",
            "planlagtTid": 6,
            "faktiskTid": 8,
            "linje": 60,
            "stopp": "Jakobs kirke"
        },
        {
            "type": "trikk",
            "navn": "Jernbanetorget",
            "planlagtTid": 2,
            "faktiskTid": 3,
            "linje": 17,
            "stopp": "Nybrua"
        },
        {
            "type": "buss",
            "navn": "Grünerløkka",
            "planlagtTid": 5,
            "faktiskTid": 5,
            "linje": 30,
            "stopp": "Jakobs kirke"
        },
        {
            "type": "trikk",
            "navn": "Holbergs plass",
            "planlagtTid": 3,
            "faktiskTid": 4,
            "linje": 19,
            "stopp": "Nybrua"
        },
        {
            "type": "buss",
            "navn": "Bislett",
            "planlagtTid": 4,
            "faktiskTid": 5,
            "linje": 21,
            "stopp": "Jakobs kirke"
        },
        {
            "type": "trikk",
            "navn": "Nationaltheatret",
            "planlagtTid": 6,
            "faktiskTid": 6,
            "linje": 13,
            "stopp": "Nybrua"
        }
    ];

    // Sorter ruter etter faktiskTid og begrens til amount
    let sortedRuter = [...ruter].sort((a, b) => a.faktiskTid - b.faktiskTid).slice(0, amount);

    // Grupper ruter etter stopp
    let groupedRuter = sortedRuter.reduce((acc: { [key: string]: RuteType[] }, rute) => {
        // Hvis stoppet ikke finnes i accumulatoren, opprett en ny array for det stoppet
        if (!acc[rute.stopp]) {
            acc[rute.stopp] = [];
        }
        // Legg til ruten i arrayen for det aktuelle stoppet
        acc[rute.stopp].push(rute);
        return acc;
    }, {});
</script>

<div class="body">
    <h2>Kollektivtransport</h2>
    <div class="line">hei</div>
    {#each Object.keys(groupedRuter).sort() as stopp}
        <h3 class="regular">{stopp}</h3>
        {#each groupedRuter[stopp] as rute}
            <Rute type={rute.type} navn={rute.navn} planlagtTid={rute.planlagtTid} faktiskTid={rute.faktiskTid} linje={rute.linje}/>
        {/each}
    {/each}
</div>

<style>
    .line {
        width: 90%;
        background-color: #707070;
    }

    .body {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100%;
        width: 98%;
        background-color: #252424;
        margin: 0 auto;
        margin-top: 24px;
        border-radius: 26px;
        padding: 16px;
        gap: 4px;
        color: white;
    }

    h3 {
        align-self: flex-start;
        margin-left: 32px;
    }
</style>