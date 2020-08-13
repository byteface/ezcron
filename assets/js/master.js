// --- countdown timer
var _second = 1000;
var _minute = _second * 60;
var _hour = _minute * 60;
var _day = _hour * 24;

function showRemaining(cron_date, el, timerid) {
	var end = new Date(cron_date);
	var now = new Date();
	var distance = end - now;
	if (distance < 0) {
		console.log('still running?')
		clearInterval(eval(timerid));
		document.getElementById(el).innerHTML = 'EXPIRED! <a href="/">🔄</a>)';
		return;
	}
	var days = Math.floor(distance / _day);
	var hours = Math.floor((distance % _day) / _hour);
	var minutes = Math.floor((distance % _hour) / _minute);
	var seconds = Math.floor((distance % _minute) / _second);

	document.getElementById(el).innerHTML = days + 'days ';
	document.getElementById(el).innerHTML += hours + 'hrs ';
	document.getElementById(el).innerHTML += minutes + 'mins ';
	document.getElementById(el).innerHTML += seconds + 'secs';
}

// --- TODO - use client to update all the calendars
function update_calendars() {

}


$(document).on('input propertychange paste', '.in_cron', function() {
	var _id = $(this).attr('id');
	var _value = $(this).val();
	var id_count = _id.split('').pop();
	var target_id = 'hr'+id_count
	redraw( target_id, '/cron_description?cron='+_value+'&id='+target_id);
});


// $(document).ready(function() {});