function updateRanking() {
    $.ajax({
        url: '/stats/ranking/',
        method: 'GET',
        success: function (data) {
            $('#ranking-container').html(renderRanking(data));
            $('#last-updated').text('Last updated: ' + new Date().toLocaleTimeString());
        },
        error: function (error) {
            console.error('Error fetching ranking:', error);
        }
    });
}

function renderRanking(data) {
    let html = '';
    data.forEach(function (stat, index) {
        html += `<tr><td>${index + 1}</td><td>${stat.player.nickname}</td><td>${stat.score}</td></tr>`;
    });
    return html;
}

function exportToCSV() {
    $.ajax({
        url: '/stats/ranking/',
        method: 'GET',
        success: function (data) {
            data.forEach((stat, index) => {
                stat.rank = index + 1;
            });

            const csvData = data.map(stat => ({
                Rank: stat.rank,
                Player: stat.player.nickname,
                Score: stat.score,
            }));

            const csv = Papa.unparse(csvData, {
                quotes: true,
                header: true,
            });

            const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');

            if (link.download !== undefined) {
                const url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', 'top_scores.csv');
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            } else {
                // for older browsers that don't support the download attribute
                navigator.msSaveBlob(blob, 'top_scores.csv');
            }
        },
        error: function (error) {
            console.error('Error exporting to CSV:', error);
        },
    });
}


// initial update (on page load)
updateRanking();

// updates every 10 seconds
setInterval(updateRanking, 10000);