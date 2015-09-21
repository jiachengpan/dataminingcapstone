
function constructGraph(data) {
  var graph = {
    nodes: [],
    links: [],
  };
  for (var node of data.meta.categories) {
    graph.nodes.push({
      name: node,
      group: 0,
    });
  }

  for (var link of data.data) {
    graph.links.push({
      source: link[0],
      target: link[1],
      value: link[2],
    })
  }

  return graph;
}

function drawForceLayout(selector, graph, meta) {
  function modifier(val) {
    if (val < 0.3) return 0;
    return val * val;
  }

  var width = 960,
      height = 960;
  
  var color = d3.scale.category20();
  
  var force = d3.layout.force()
      .charge(-120)
      .linkDistance(30)
      .size([width, height]);
  
  var svg = d3.select(selector).append("svg")
      .attr("width", width)
      .attr("height", height);

  force
      .nodes(graph.nodes)
      .links(graph.links)
      .linkDistance(function(d) { return d.value * 400 + 100})
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", function(d)    { return 1; })
      .style("stroke-opacity", function(d)  { return modifier(1 - d.value); })

  var node = svg.selectAll(".node")
      .data(graph.nodes)
    .enter().append('g')
      .attr("class", "node")
      .call(force.drag);
    
  node.append("circle")
      .attr("r", 5)
      .style("fill", function(d) { return color(d.group); });


  node.append("text")
      .text(function(d) { return d.name; })
      .attr("class", "mono");

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
}


function drawMatrix(selector, data, draw_cluster) {
  var margin = {top: 200, right: 0, bottom: 10, left: 200},
      width = 900,
      height = 900;
  
  var x = d3.scale.ordinal().rangeBands([0, width]),
      z = d3.scale.linear().domain([1, 0])//.clamp(true),
      c = d3.scale.category10().domain(d3.range(10));
  
  var svg = d3.select(selector).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .style("margin-left", -margin.left + "px")
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var matrix = [],
      nodes = [],
      n = data.meta.categories.length;

  for (var i in data.meta.categories) {
    nodes.push({
      name: data.meta.categories[i],
      index: i,
      group: data.cluster ? data.cluster[i] : 0,
    });
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 1}; });
  }

  for (var i in data.data) {
    var src = data.data[i][0];
    var dst = data.data[i][1];
    var val = data.data[i][2];

    matrix[src][dst].z = val;
    matrix[dst][src].z = val;
  }

  console.log(matrix)

  // Precompute the orders.
  var orders = {
    name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
    group: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
  };

  // The default sort order.
  x.domain(orders.name);

  svg.append("rect")
      .attr("class", "background")
      .attr("width", width)
      .attr("height", height);

  var row = svg.selectAll(".row")
      .data(matrix)
    .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .each(row);

  row.append("line")
      .attr("x2", width);

  row.append("text")
      .attr("x", -6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .text(function(d, i) { return nodes[i].name; });

  var column = svg.selectAll(".column")
      .data(matrix)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column.append("line")
      .attr("x1", -width);

  column.append("text")
      .attr("x", 6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .text(function(d, i) { return nodes[i].name; });

  function row(row) {
    var cell = d3.select(this).selectAll(".cell")
        //.data(row.filter(function(d) { return d.z; }))
        .data(row)
      .enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return z(d.z); })
        //.style("fill", function(d) { return nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : null; })
        .style("fill", function(d) {
          if (!draw_cluster || !data.cluster) return '#000000';
          return nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : '#000000';
        })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);
  }

  function mouseover(p) {
    d3.selectAll(".row text").classed("active", function(d, i) { return i == p.y; });
    d3.selectAll(".column text").classed("active", function(d, i) { return i == p.x; });
  }

  function mouseout() {
    d3.selectAll("text").classed("active", false);
  }

  d3.select("#order").on("change", function() {
    clearTimeout(timeout);
    order(this.value);
  });

  function order(value) {
    x.domain(orders[value]);

    var t = svg.transition().duration(2500);

    t.selectAll(".row")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .selectAll(".cell")
        .delay(function(d) { return x(d.x) * 4; })
        .attr("x", function(d) { return x(d.x); });

    t.selectAll(".column")
        .delay(function(d, i) { return x(i) * 4; })
        .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });
  }

  var timeout = setTimeout(function() {
    order("group");
    d3.select("#order").property("selectedIndex", 2).node().focus();
  }, 5000);

}

function draw(path, draw_cluster) {
  $.getJSON(path, function(data) {
    var range = [];
    for (var i = 0; i < data.meta.categories.length; i++) {
      range.push(i);
    }

    //drawForceLayout('#force', constructGraph(data), data.meta);

    drawMatrix('#matrix', data, draw_cluster);

    return
    
    var upper = data.data.length;
    for (var i = 0; i < upper; i++) {
      if (data.data[i][0] == data.data[i][1]) continue;
      data.data.push([data.data[i][1], data.data[i][0], data.data[i][2]]);
    }
    
    $('#matrix').highcharts('Map', {
      series: [{
        type: 'heatmap',
        name: 'similarity',
        data: data.data,
        tooltip: {
          headerFormat: 'Similarity<br/>',
          pointFormatter: function() {
            return data.meta.categories[this.x] + ' vs ' +
              data.meta.categories[this.y] + ' : ' + 
              this.value.toFixed(4);
          }
        },
      }],
      chart: {
        type: 'heatmap',
        height: 800,
      },
      title: {
        text: 'Task 2.1',
      },
      xAxis: {
        min: 0,
        max: data.meta.categories.length,
        tickPositions: range,
        labels: {
          rotation: 45,
          formatter: function() {
            return data.meta.categories[this.value];
          }, 
        },
      },
      yAxis: {
        min: 0,
        max: data.meta.categories.length,
        tickPositions: range,
        labels: {
          formatter: function() {
            return data.meta.categories[this.value];
          }, 
        }
      },
      colorAxis: {
        min: 0,
        max: 1,
        minColor: '#000000',
        maxColor: '#ffffff',
      },
    });
  });
}
