$(document).ready(function() {
    var now = new Date();
    // month is... 0-indexed?? ? ?
    var then = new Date(2019, 2, 11);
    var diff = (now.getTime() - then.getTime()) / 1000;
    var clock = $('.clock').FlipClock(diff, {
        clockFace: 'DailyCounter',
    });
});
