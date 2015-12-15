
// var color_list = ["rgba(220,220,220,0.2)"]
// var d1 = [10.21,10.31,10.31,10.31,10.31,15.31,10.31,10.31,56.31,10.31, 44.31,10.31,]
// var d2 = [10,10,10,10,10,10,10,10,10,10, 10,10,]
// var d3 = [0,0,0,0,0,0,0,0,0,0,0,0,]
// var special_data = {
//     labels: ['start', " ", " ", " ", " ", " "," ", " ", " ", " ", " ", 'end'],
//     datasets: [{
//         label: "aaa",
//         fillColor: "rgba(151,187,205,0.2)",
//         strokeColor: "rgba(151,187,205,1)",
//         pointColor: "rgba(151,187,205,1)",
//         pointStrokeColor: "#fff",
//         pointHighlightFill: "#fff",
//         pointHighlightStroke: "rgba(151,187,205,1)",
//         data: d3
//       },]
//   };




function random_numb(Max, Min){
	var range = Max - Min;
	var rand  = Math.random()
	return (Min + Math.round(rand*range))
}

function color_generation(){
	var Max = 250;
	var Min = 50;
	var r = random_numb(Max, Min)
	var g = random_numb(Max, Min)
	var b = random_numb(Max, Min)
	return "rgba("+r.toString()+","+g.toString()+","+b.toString()+",1)"
}

function datasets(label,color, data){
  return {
  	label: label,
  	fillColor: "rgba(0,0,0,0)",
    strokeColor: color,
    pointColor: color,
    pointStrokeColor: "#fff",
    pointHighlightFill: "#fff",
    pointHighlightStroke: color,
    data: data
  }
}


function disk_data(all_info, field){

	var disk_name = all_info['diskName'];
	var disk_info_dic = all_info['disk'];

	console.log(disk_info_dic)

	var dataset_array = new Array();
	for(var i=0; i<disk_name.length; i++){
		dataset_array[i] = datasets(disk_name[i], color_generation(), 
									disk_info_dic[disk_name[i]][field])
	}
	console.log(dataset_array);
	return {
		labels: all_info['times'],
		datasets: dataset_array
	}
}


$(function(){

 
  var CPU_Usage = null;
  var CPU_Load = null;
  var Mem_Usage = null;
  var Process_Numb = null;

  $.getJSON('/openstack/data/', function(data){
    if (data){
   	  //console.log(data)
	  //console.log(disk_data(data, 'kb_read'))
	  var ctx = $("#memUsage").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(chart_data(data['memUsage'], data['times']),{scaleLabel : "<%=value%>%",});

      var ctx = $("#tps").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(disk_data(data, 'tps'), {
      								   scaleLabel : "<%=value%>",
      								   multiTooltipTemplate: "<%=datasetLabel%>:<%=value%>"});
      var ctx = $("#kb_read").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(disk_data(data, 'kb_read'), {
      								   scaleLabel : "<%=value%>MB",
      								   multiTooltipTemplate: "<%=datasetLabel%>:<%=value%>"});
      var ctx = $("#kb_write").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(disk_data(data, 'kb_write'), {
      								   scaleLabel : "<%=value%>MB",
      								   multiTooltipTemplate: "<%=datasetLabel%>:<%=value%>"});
      var ctx = $("#speed_kb_read").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(disk_data(data, 'speed_kb_read'), {
      								   scaleLabel : "<%=value%>kB/s",
      								   multiTooltipTemplate: "<%=datasetLabel%>:<%=value%>"});
      var ctx = $("#speed_kb_write").get(0).getContext("2d");
      var myLineChart = new Chart(ctx).Line(disk_data(data, 'speed_kb_write'), {
      								   scaleLabel : "<%=value%>kB/s",
      								   multiTooltipTemplate: "<%=datasetLabel%>:<%=value%>"});
      
      
    }
  
  });
})