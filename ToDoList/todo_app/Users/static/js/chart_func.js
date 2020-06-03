var x_values_str = String(document.getElementById('x_values').textContent);
var x_values = x_values_str.replace('[', '').replace(']', '');
for (let index = 0; index < x_values.length; index++) {
    x_values = x_values.replace("'", '')
}
x_values = x_values.split(',')

var y_values_str = String(document.getElementById('y_values').textContent);
var y_values = y_values_str.replace('[', '').replace(']', '');
for (let index = 0; index < y_values.length; index++) {
    y_values = y_values.replace("'", '')
}
y_values = y_values.split(',')


var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: x_values,
        datasets: [{
            label: 'Your progress through',
            data: y_values,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});