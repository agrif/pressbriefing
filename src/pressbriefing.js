function updateClock() {
    var now = new Date();
    var then = Date.parse(info.date);
    var diff = (now.getTime() - then) / 1000;
    var clock = $('.clock').FlipClock(diff, {
        clockFace: 'DailyCounter',
        showSeconds: false,
    });
    $('.latest').html(
        '<a href="' + info['url'] + '">' + info['title'] + '</a>'
    );
}

$(document).ready(function() {
    updateClock();
});
