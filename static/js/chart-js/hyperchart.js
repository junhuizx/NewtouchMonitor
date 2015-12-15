

// var data = {
//     labels: ['start', " ", " ", " ", " ", " "," ", " ", " ", " ", " ", 'end'],
//     datasets: [
//       {
//         label: "My Second dataset",
//         fillColor: "rgba(151,187,205,0.2)",
//         strokeColor: "rgba(151,187,205,1)",
//         pointColor: "rgba(151,187,205,1)",
//         pointStrokeColor: "#fff",
//         pointHighlightFill: "#fff",
//         pointHighlightStroke: "rgba(151,187,205,1)",
//         data: [65, 59, 80, 81, 56, 15, 40, 80, 81, 56, 55, 40]
//       },
//     ]
//   };



$(function(){
  var CPU_Usage = null;
  var CPU_Load = null;
  var Mem_Usage = null;
  var Process_Numb = null;

  $.getJSON('/server/chart/', function(data){
    if (data){
      var keys = data['times']
      CPU_Usage=chart_data(data['cpuUsage'],keys)
      CPU_Load=chart_data(data['cpuLoad'], keys)
      Mem_Usage=chart_data(data['memUsage'],keys)
      Process_Numb=chart_data(data['procNumb'], keys)

      var ctx = $("#cpuUsage").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(CPU_Usage,
                                            {scaleLabel : "<%=value%>%"});
      var ctx = $("#memUsage").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(Mem_Usage,
                                            {scaleLabel : "<%=value%>%"});

      var ctx = $("#procNumb").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(Process_Numb);

      var ctx = $("#cpuLoad").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(CPU_Load);

      
      
    }
  
  });

})
