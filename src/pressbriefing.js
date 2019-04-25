$(document).ready(function() {
    var now = new Date();
    var then = Date.parse(info.date);
    var diff = (now.getTime() - then) / 1000;
    var clock = $('.clock').FlipClock(diff, {
        clockFace: 'DailyCounter',
    });
});
