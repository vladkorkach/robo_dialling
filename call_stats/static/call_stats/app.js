var chartObj = document.getElementById("src_data").innerText;

chartObj = JSON.parse(chartObj);

if(chartObj.dataProvider.length === 0) {
    document.getElementById('chartdiv').innerHTML = "No data to show";
} else {
    var chart1 = AmCharts.makeChart("chartdiv", chartObj);
}
