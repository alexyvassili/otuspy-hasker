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
		  		$(qtag).text(data);
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
			},
			error: function(){
				console.log('ERROR');	
			}
		})
	})
});
