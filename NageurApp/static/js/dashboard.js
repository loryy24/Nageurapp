let bpmData = [];
let labels = [];
let chart;

function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('mouvement_bras').textContent = data.mouvement_bras;
            document.getElementById('bpm_moyen').textContent = data.bpm_moyen;
            document.getElementById('swolf').textContent = data.swolf;
            document.getElementById('vitesse').textContent = data.vitesse;
            document.getElementById('niveau_batterie').textContent = data.niveau_batterie;

            if (bpmData.length > 20) {
                bpmData.shift();
                labels.shift();
            }

            bpmData.push(data.bpm_instant);
            labels.push(new Date().toLocaleTimeString());

            chart.update();
        });
}

window.onload = function () {
    const ctx = document.getElementById('bpmChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'BPM instantané',
                data: bpmData,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    fetchData();
    setInterval(fetchData, 2000);
};
