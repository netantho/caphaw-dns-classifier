$( document ).ready(function() {
  $('#myTabs a').click(function (e) {
    e.preventDefault()
    //the previously active tab
    var prev = $('#myTabs .active a').attr("href");

    //the tab we want to activate
    var target = $(e.target).attr('href');

    //deactivate the current tab
    var p = $('#myTabs a[href="' + prev + '"]')
    p.parent().removeClass('active');

    //activate the new one
    var n = $('#myTabs a[href="' + target + '"]');
    n.parent().addClass('active');

    //display the new one
    $(prev).hide();
    $(target).show();
  });

});

