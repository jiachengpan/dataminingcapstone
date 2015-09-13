Math.seed = function(s) {
    return function() {
        s = Math.sin(s) * 10000;
        return s - Math.floor(s);
    };
};

var random = Math.seed(24);

(function () {
  var fill = d3.scale.category20();
  var width = 600,
      height= 400;

  var topicIdx = 0;

  function draw(data) {
    var svg = d3.select('div.container').append('svg')
      .attr('style', 'display: block')
      .attr('width', width)
      .attr('height', height);

    svg.append('g')
      .append('text')
        .attr('transform', 'translate(0 40)')
        .style('font-size', 16)
        .style('font-weight', 'bold')
        .style("font-family", "monospace")
        .style('fill', 'black')
        .text('TOPIC ' + topicIdx);

    svg.append('g')
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
    .selectAll('text')
      .data(data)
    .enter().append('text')
      .style("font-size", function(d) { return d.size + "px"; })
      .style("font-family", "Impact")
      .style("fill", function() { return fill(topicIdx); })
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) { return d.text; });
  }

  $.getJSON(datafile, function(data) {
    for (var topic of data) {
      var values = [];
      var sum = 0;
      for (var t in topic) {
        values.push(parseFloat(topic[t]));
        sum += parseFloat(topic[t]);
      }
      var max = Math.max.apply(null, values);
      words = [];
      for (var word in topic) {
        words.push({
          text: word,
          size: parseFloat(topic[word]) / max * 60,
        });
      }

      var layout = d3.layout.cloud()
        .size([width, height])
        .padding(1)
        .font('Impact')
        .fontSize(function (d) { return (d.size < 3) ? 3 : d.size; })
        //.rotate(function() { return 0; })
        .rotate(function() { return (random() > 0.7 ? -90: 0); })
        .words(words)
        .on('end', draw);
      layout.start();

      topicIdx += 1;
    }

  });
})();
