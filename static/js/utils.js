// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

async function fetchAPI(url) {       
    try {
        const response = await fetch(url);
        
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;

    } catch (error) {
        // Catch network issues or parsing failures
        console.error("Fetch operation failed:", error.message);
    }
}

function loadOysterGraph(ctx, token){
    fetchAPI("/api/oyster/get?token=" + token).then(oysterData => {
        var data = [[oysterData.name]];
        oysterData.oysterlog_set.forEach(element => {
            data[0].push([element.date, parseFloat(element.ph_level)]);
        });

        const datasets = data.map((series, index) => {
            return {
                label: `${series[0]}`,
                data: series.slice(1, series.length).map(item => ({
                    x: item[0],
                    y: item[1],
                })),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.2
            };
        });

        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: datasets
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'pH Level'
                        },
                        min: 0,
                        max: 14,
                    }
                }
            }
        });
    });
}