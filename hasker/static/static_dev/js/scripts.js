var process_rate = function(data, tag, like) {
	$(tag).text(data);
	if (data < 0) {
		$(tag).removeClass("btn-outline-success");
		$(tag).addClass("btn-outline-danger");
	}
	else{
		$(tag).removeClass("btn-outline-danger");
		$(tag).addClass("btn-outline-success");
	}

	if (like == 'like') {
		$(tag).prev().removeClass("btn-dark").addClass("btn-outline-dark");
		$(tag).next().removeClass("btn-outline-dark").addClass("btn-dark");
	}
	else {
		$(tag).prev().removeClass("btn-outline-dark").addClass("btn-dark");
		$(tag).next().removeClass("btn-dark").addClass("btn-outline-dark");
	}
}

$(document).ready(function(){
	$('.btn-question-dislike').on('click', function(e){
		e.preventDefault();
		url = "/q/" + this.id + "/dislike/";
		qid = this.id;
		postedData = "";
		$.ajax({
		  type: 'GET',
		  url: url,
		  data: postedData,
		  success: function(data) {
		  		var qtag = '#qrate_' + qid;
		  		process_rate(data, qtag, 'dislike');
			},
			error: function(){
				console.log('ERROR');	
			}
		})
	})

	$('.btn-question-like').on('click', function(e){
		e.preventDefault();
		console.log('CLICK');
		console.log(this.id);
		var qid = this.id;
		url = "/q/" + this.id + "/like/";
		postedData = "";
		$.ajax({
		  type: 'GET',
		  url: url,
		  data: postedData,
		  success: function(data) {
		  		var qtag = '#qrate_' + qid;
		  		$(qtag).text(data);
		  		process_rate(data, qtag, 'like');
			},
			error: function(){
				console.log('ERROR');	
			}
		})
	})

	$('.btn-answer-dislike').on('click', function(e){
		e.preventDefault();
		console.log('CLICK');
		console.log(this.id);
		url = "/q/answer/" + this.id + "/dislike/";
		var aid = this.id;
		postedData = "";
		$.ajax({
		  type: 'GET',
		  url: url,
		  data: postedData,
		  success: function(data) {
		  		var atag = '#arate_' + aid;
		  		$(atag).text(data);
		  		process_rate(data, atag, 'dislike');
			},
			error: function(){
				console.log('ERROR');	
			}
		})
	})

	$('.btn-answer-like').on('click', function(e){
		e.preventDefault();
		console.log('CLICK');
		console.log(this.id);
		url = "/q/answer/" + this.id + "/like/";
		var aid = this.id;
		postedData = "";
		$.ajax({
		  type: 'GET',
		  url: url,
		  data: postedData,
		  success: function(data) {
		  		var atag = '#arate_' + aid;
		  		$(atag).text(data);
		  		process_rate(data, atag, 'like');
			},
			error: function(){
				console.log('ERROR');	
			}
		})
	})

	$('.ajax_solution_button').on('click', function(e){
		e.preventDefault();
		console.log('CLICK SOLUTION');
		console.log(this.id);
		url = "/q/answer/" + this.id + "/is_solution/";
		var aid = this.id;
		postedData = "";
		$.ajax({
		  type: 'GET',
		  url: url,
		  data: postedData,
		  success: function(data) {
		  		console.log(data);
		  		var btn_cls = '.sol_' + aid;
		  		$(btn_cls).text("");
		  		$(btn_cls).removeClass( "btn-outline-success" ).addClass( "btn-success" );
		  		$(btn_cls).append('<i data-feather="check"></i>&nbsp;Marked as solution');
		  		feather.replace();
			},
			error: function(){
				console.log('ERROR');	
			}
		})
	})
});
