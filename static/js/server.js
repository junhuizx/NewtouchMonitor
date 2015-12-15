
var defaults = {
  scaleOverlay : false,
    
    //Boolean - If we want to override with a hard coded scale
    scaleOverride : true,
    
    //** Required if scaleOverride is true **
    //Number - The number of steps in a hard coded scale
    scaleSteps : 10,
    
    //Number - The value jump in the hard coded scale
    scaleStepWidth : 10,
    
    // Y 轴的起始值
    scaleStartValue : 0,

    // Y/X轴的颜色
    scaleLineColor : "rgba(0,0,0,.1)",
    
    // X,Y轴的宽度
    scaleLineWidth : 1,

    // 刻度是否显示标签, 即Y轴上是否显示文字
    scaleShowLabels : true,
    
    // Y轴上的刻度,即文字
    scaleLabel : "<%=value%>%",
    
    // 字体
    scaleFontFamily : "'Arial'",
    
    // 文字大小
    scaleFontSize : 12,
    
    // 文字样式
    scaleFontStyle : "normal",
    
    // 文字颜色
    scaleFontColor : "#666",  
    
    // 是否显示网格
    scaleShowGridLines : true,
    
    // 网格颜色
    scaleGridLineColor : "rgba(0,0,0,.05)",
    
    // 网格宽度
    scaleGridLineWidth : 2, 
    
    // 是否使用贝塞尔曲线? 即:线条是否弯曲
    bezierCurve : true,
    
    // 是否显示点数
    pointDot : true,
    
    // 圆点的大小
    pointDotRadius : 8,
    
    // 圆点的笔触宽度, 即:圆点外层白色大小
    pointDotStrokeWidth : 2,
    
    // 数据集行程
    datasetStroke : true,
    
    // 线条的宽度, 即:数据集
    datasetStrokeWidth : 2,
    
    // 是否填充数据集
    datasetFill : false,
    
    // 是否执行动画
    animation : true,

    // 动画的时间
    animationSteps : 60,
    
    // 动画的特效
    animationEasing : "easeOutQuart",

    // 动画完成时的执行函数
    onAnimationComplete : null,

    // show label by datasets label value in mutli lines diagram
    multiTooltipTemplate: "<%= datasetLabel %> - <%= value %>"
}




function chart_data(data, keys){

  var data = {
    labels: keys,
    datasets: [
      {
        label: "cpu",
        fillColor: "rgba(0,0,0,0)",
        // fillColor: "rgba(151,187,205,0.2)",
        strokeColor: "rgba(151,187,205,1)",
        pointColor: "rgba(151,187,205,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(151,187,205,1)",
        data: data
      },
    ]
  };
  
  return data

} 

$(function(){
  $('.host_ip').click(function(){
    var monitor_host_ip = $(this).text();
    var agent_ip = $(this).attr('agent');
    $.getJSON('/server/host/', 
              {'host_ip':monitor_host_ip,
               'agent_ip':agent_ip}, function(){});
    location.href = '/server/monitor/detail/';

  });
})

$(function(){
  $('.gradeX .instance').click(function(){
    var uuid = $(this).attr('id');
    var ops_agent = $(this).parent('td').attr('class');
    console.log(uuid);
    console.log(ops_agent);
    $.getJSON('/openstack/uuid/', 
              {'uuid':uuid, 'ops_agent':ops_agent}, function(){});
    location.href = '/openstack/detail/';

  })

})

$(function(){
    $('a.pull-right.btn.btn-primary').click(function(){
        var idc_id = $('.nav.nav-tabs li.active a').attr('idc');
        console.log(idc_id);
        location.href = '/server/manager/add/?idc_id='+idc_id


    })
})
