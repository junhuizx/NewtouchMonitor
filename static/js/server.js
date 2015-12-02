
$(function(){
  $('.host_ip').click(function(){
    console.log('in host_ip');
    monitor_host_ip = $(this).text();
    console.log(monitor_host_ip);
    $.getJSON('/server/host/', {'host_ip':monitor_host_ip}, function(){});
    location.href = '/server/monitor/detail/';

  });
})                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              