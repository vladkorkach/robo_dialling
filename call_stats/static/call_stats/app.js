var chartObj = document.getElementById("src_data").innerText;
console.log(chartObj)
var chart1 = AmCharts.makeChart("chartdiv",
  JSON.parse(chartObj)
  // type: "serial",
  // theme: "light",
  // dataProvider: [{'date': '2018-11-27 18-37-15', 'Yahoo': 18, 'Google': 18}, {'date': '2018-11-27 18-37-45', 'Yahoo': 18, 'Google': 18}, {'date': '2018-11-27 18-38-15', 'Yahoo': 18, 'Google': 18}, {'date': '2018-11-27 18-38-45', 'Google': 18, 'Yahoo': 18}, {'date': '2018-11-27 18-39-15', 'Yahoo': 18, 'Google': 18}, {'date': '2018-11-27 18-39-45', 'Google': 18, 'Yahoo': 18}, {'date': '2018-11-27 18-40-15', 'Yahoo': 18, 'Google': 9}, {'date': '2018-11-27 18-40-16', 'Google': 9}, {'date': '2018-11-27 18-40-45', 'Google': 9, 'Yahoo': 9}, {'date': '2018-11-27 18-40-46', 'Google': 9, 'Yahoo': 9}, {'date': '2018-11-27 18-41-15', 'Google': 9, 'Yahoo': 9}],
  // graphs: [
  //   {
  //     "bullet": "round",
  //     valueField: "Yahoo",
  //       "labelText": "[[key]]",
  //       title:"yahoo"
  //   },
  //     {
  //     bullet: "round",
  //     valueField: "Google",
  //         "labelText": "[[key]]",
  //         title:"google"
  //   }
  // ],
  //   "legend": {
  //       "useGraphSettings": true,
  // },
  // categoryField: "date",
  // dataDateFormat: "YYYY-MM-DD JJ:NN:SS",
  // categoryAxis: {
  //   parseDates: true,
  //   minPeriod: "ss"
  // }
);

// chart1.startEffect = "easeInSine";
// chart1.startDuration = "0.7";
// chart1.sequencedAnimation = document.getElementById("sequenced").checked;
// chart1.animateAgain();
