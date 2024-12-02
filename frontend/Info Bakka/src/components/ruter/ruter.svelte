<script lang="ts">
    import Rute from "./rute.svelte";
    export let amount: number = 10;

    interface EstimatedCall {
        realtime: boolean;
        aimedDepartureTime: string;
        expectedDepartureTime: string;
        destinationDisplay: {
            frontText: string;
        };
        serviceJourney: {
            journeyPattern: {
                line: {
                    id: string;
                    name: string;
                };
            };
        };
    }

    interface EnturResponse {
        data: {
            stopPlace: {
                id: string;
                name: string;
                estimatedCalls: EstimatedCall[];
            };
        };
    }

    let ruter: EstimatedCall[] = [];

    // Function to calculate minutes until departure
    function getMinutesUntilDeparture(expectedTime: string): number {
        const now = new Date();
        const departure = new Date(expectedTime);
        return Math.round((departure.getTime() - now.getTime()) / 60000);
    }

    // Function to get line number from line ID
    function getLineNumber(lineId: string): number {
        return parseInt(lineId.split(':').pop() || '0');
    }

    // Function to determine transport type from line ID
    function getTransportType(lineId: string): string {
        if (!lineId) return 'unknown';
        
        // Handle RUT (Ruter) format
        if (lineId.startsWith('RUT:Line:')) {
            // Get the line number
            const lineNumber = parseInt(lineId.split(':').pop() || '0');
            
            // Ruter official line numbering:
            if ([1, 2, 3, 4, 5, 6].includes(lineNumber)) return 't-bane';  // Metro lines are 1-6
            if ([11, 12, 13, 17, 18, 19].includes(lineNumber)) return 'trikk';  // Tram lines
            // Bus lines according to Ruter's website
            if ((lineNumber >= 20 && lineNumber <= 28) || // Bus group 20-28
                (lineNumber >= 30 && lineNumber <= 37) || // Bus group 30-37
                (lineNumber >= 40 && lineNumber <= 48) || // Bus group 40-48
                (lineNumber >= 51 && lineNumber <= 58) || // Bus group 51-58
                (lineNumber >= 60 && lineNumber <= 69) || // Bus group 60-69
                (lineNumber >= 70 && lineNumber <= 79) || // Bus group 70-79
                (lineNumber >= 80 && lineNumber <= 87))   // Bus group 80-87
                return 'buss';
        }
        
        // Log unknown types to help identify missing mappings
        console.log('Unknown transport type for lineId:', lineId);
        return 'unknown';
    }

    // Fetch data from the backend
    async function fetchData() {
        try {
            const response = await fetch('http://localhost:8000/data');
            const reader = response.body?.getReader();
            if (!reader) return;

            while (true) {
                const {value, done} = await reader.read();
                if (done) break;

                const text = new TextDecoder().decode(value);
                // Split by double newline to handle the streaming format
                const chunks = text.split('\n\n');
                
                for (const chunk of chunks) {
                    if (chunk.trim()) {  // Only process non-empty chunks
                        try {
                            const data: EnturResponse = JSON.parse(chunk);
                            if (data.data?.stopPlace?.estimatedCalls) {
                                ruter = data.data.stopPlace.estimatedCalls
                                    .slice(0, amount);  // Limit to amount
                            }
                        } catch (parseError) {
                            console.error('Error parsing chunk:', parseError);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // Add onMount to start the data fetching
    import { onMount } from 'svelte';

    onMount(() => {
        fetchData();
    });

    // Function to format time display
    function formatTime(minutes: number): string {
        return minutes === 0 ? 'Nå' : minutes.toString();
    }
</script>

<div class="body">
    <h2>Kollektivtransport</h2>
    <div class="line"></div>
    {#each ruter as rute}
        {console.log('Line ID:', rute.serviceJourney.journeyPattern.line.id)}
        <Rute 
            type={getTransportType(rute.serviceJourney.journeyPattern.line.id)}
            navn={rute.destinationDisplay.frontText}
            planlagtTid={formatTime(getMinutesUntilDeparture(rute.aimedDepartureTime))}
            faktiskTid={formatTime(getMinutesUntilDeparture(rute.expectedDepartureTime))}
            linje={getLineNumber(rute.serviceJourney.journeyPattern.line.id)}
        />
    {/each}
</div>

<style>
    .line {
        width: 90%;
        height: 1px;
        background-color: #707070;
        margin: 8px 0;
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