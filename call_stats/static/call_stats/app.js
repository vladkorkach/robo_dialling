var chartObj = document.getElementById("src_data").innerText;
chartObj = JSON.parse(chartObj)
console.log()
if(chartObj.dataProvider.length === 0) {
  document.getElementById('chartdiv').innerHTML = "No data to show";
} else {
  var chart1 = AmCharts.makeChart("chartdiv", chartObj);
}

// chart1.startEffect = "easeInSine";
// chart1.startDuration = "0.7";
// chart1.sequencedAnimation = document.getElementById("sequenced").checked;
// chart1.animateAgain();
