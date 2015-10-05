
function draw(path) {
  var margin = {top: 20, right: 20, bottom: 140, left: 80},
      width = 960 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom;
  
  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);
  
  var y = d3.scale.linear()
      .range([height, 0]);

  var color = d3.scale.linear()
      .range(['red', 'green']);
  
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");
  
  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(10)
  
  var svg = d3.select("#plot").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  d3.json(path, function(error, data) {
    if (error) throw error;

    data = data.slice(data.length - 50);
  
    x.domain(data.map(function(d) { return d.name; }));
    y.domain([0.1 * d3.min(data, function(d) { return d.freq; }), d3.max(data, function(d) { return d.freq; })]);
    color.domain([d3.min(data, function(d) { return d.score; }), d3.max(data, function(d) { return d.score; })]);

  
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
          .selectAll('text')
          .style("text-anchor", "end")
          .attr("dx", "-.8em")
          .attr("dy", ".15em") 
          .attr("transform", "rotate(-55)")
  
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Occurrence");
  
    svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr('fill', function(d) { return color(d.score); })
        .attr("x", function(d) { return x(d.name); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.freq); })
        .attr("height", function(d) { return height - y(d.freq); });
  });
}



function draw_rest(path) {

  var margin = {top: 20, right: 20, bottom: 140, left: 80},
      width = 960 - margin.left - margin.right,
      height = 600 - margin.top - margin.bottom;
  
  var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);
  
  var y = d3.scale.linear()
      .range([height, 0]);

  var color = d3.scale.linear()
      .range(['red', 'green']);
  
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");
  
  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(10)
  
  var svg = d3.select("#plot").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  function draw_data(data) {
    x.domain(data.map(function(d) { return d.name; }));
    y.domain([0.1 * d3.min(data, function(d) { return d.freq; }), d3.max(data, function(d) { return d.freq; })]);
    color.domain([d3.min(data, function(d) { return d.score; }), d3.max(data, function(d) { return d.score; })]);
 
    svg.select('.x.axis')
        .call(xAxis)
          .selectAll('text')
          .style("text-anchor", "end")
          .attr("dx", "-.8em")
          .attr("dy", ".15em") 
          .attr("transform", "rotate(-55)");
  
    svg.select(".y.axis")
        .call(yAxis);
  
    svg.selectAll(".bar")
        .remove();
    svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr('fill', function(d) { return color(d.score); })
        .attr("x", function(d) { return x(d.name); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.freq); })
        .attr("height", function(d) { return height - y(d.freq); })
        .attr('data-my', function(d) {return d.name + d.freq})
  }
  
  var dish_data = null
  d3.json(path, function(error, data) {
    if (error) throw error;

    dish_data = data;

    $('#dish_sel').empty();
    for (var dish in data) {
      $('#dish_sel').append('<option>' + dish + '</option>');
    }

    var dish_name = $('#dish_sel').val();

    $('#dish_sel').on('change', function() {
      dish_name = $('#dish_sel').val();
      data = dish_data[dish_name].slice();
      data = data.slice(data.length - 50);
      draw_data(data);
    })

    data = dish_data[dish_name].slice();
    data = data.slice(data.length - 50);

    x.domain(data.map(function(d) { return d.name; }));
    y.domain([0.1 * d3.min(data, function(d) { return d.freq; }), d3.max(data, function(d) { return d.freq; })]);
    color.domain([d3.min(data, function(d) { return d.score; }), d3.max(data, function(d) { return d.score; })]);

  
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
          .selectAll('text')
          .style("text-anchor", "end")
          .attr("dx", "-.8em")
          .attr("dy", ".15em") 
          .attr("transform", "rotate(-55)")
  
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Occurrence");
  
    svg.selectAll(".bar")
        .data(data.slice())
      .enter().append("rect")
        .attr("class", "bar")
        .attr('fill', function(d) { return color(d.score); })
        .attr("x", function(d) { return x(d.name); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.freq); })
        .attr("height", function(d) { return height - y(d.freq); })
        .attr('data-my', function(d) { return d.name + d.freq })
  });
}
