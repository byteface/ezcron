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

	// get each cron and color

	// for each cron. stamp a color on teh date in teh calendar
	$('.thecron').each(function(){
		
		var cron = $(this).text();
		var col = $(this).find('a').css('color');
		var s = later.parse.cron(cron);
		// window.console.log(later.schedule(s).next(10));

		var dates = later.schedule(s).next(1000); // TODO - 86400 seconds per day * 365 days
		// need to filter first on days already populated. then get count.
		// potentialy modal a 'day' view. that can show hours/minutes

		for( var i=0; i<dates.length; i++ ){
			draw_date_on_calendar(dates[i],cron,col);
		}


	});
	
	// for each record get the dates
	// for each date
	 // find the month
	 // find the day
	 // write a elements to that days number

}

function draw_date_on_calendar( date, cron, col ){
	var month = date.getMonth();
	var day = date.getDate();

	// console.log(month,day);

	var tables = $("table.month");
	var days = $(tables[month]).find('td');
	for(var i=0; i<days.length; i++){

		// console.log( $(days[i]).text() , day );

		var d = $(days[i]).text();
		d = d.split('*').join('');

		if(d == day){
			// $(days[i]).css("background","red");
			$(days[i]).append( "<a title='"+cron+"' style='color:"+col+";'>*</a>" );
			break;
		}
	}
}

// update_calendars();


$(document).on('input propertychange paste', '.in_cron', function() {
	var _id = $(this).attr('id');
	var _value = $(this).val();
	var id_count = _id.split('').pop();
	var target_id = 'hr'+id_count
	redraw( target_id, '/cron_description?cron='+_value+'&id='+target_id);
});


// $(document).ready(function() {});

window.run_job = function( line_number ){
    $.get( '/run_job?line='+line_number, function( data ) {
    	alert("RUN RAN!")
    });
}

window.create_job = function( cron, command ){
    $.get( '/update?cron='+line_number+"&command="+command, function( data ) {
    	// window.console.log(data)
    	console.log("CREATE RAN!")
    });
}

window.update_job = function( cron, command ){
    $.get( '/update?cron='+line_number+"&command="+command, function( data ) {
    	// window.console.log(data)
    	console.log("UPDATE RAN!")
    });
}

window.delete_job = function( line_number ){
    $.get( '/delete?line='+line_number, function( data ) {
    	// window.console.log(data)
    	console.log("DELETE RAN!")
    });
}

