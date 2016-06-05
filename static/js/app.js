var items = {};

$.getJSON('http://192.168.10.10:5000/postsprom.json', function(result)
	{
		window.console.log(result['promos'])
		Object.assign(items, result);

	});

function refreshPage() {
    $.getJSON('http://192.168.10.10:5000/promojson', function(result)
	{
		Object.assign(items, result);
	});

	setTimeout(function(){
		refreshPage();
	}, 10000);
}

window.setTimeout(function(){
	refreshPage();
}, 10000);

var data2 = {lista:[{"nm_prom":"1","cod":["3","4"]},{"nm_prom":"3","cod":"5"}]};

var promVue = new Vue({
	//el: "#vue",
	
	data: items,

	methods: {
		exibir: function()
		{
			window.console.log("Items variavel global");
			window.console.log(this);
		}
	}
});

new Vue({
	el: '#vue'
});