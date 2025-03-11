document.addEventListener("DOMContentLoaded", function() {
    fetch("/api/topology")
        .then(response => response.json())
        .then(data => {
            const width = 1000, height = 600;

            const svg = d3.select("#visualization")
                          .append("svg")
                          .attr("width", width)
                          .attr("height", height);

            const simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.links).id(d => d.id).distance(200))
                .force("charge", d3.forceManyBody().strength(-500))
                .force("center", d3.forceCenter(width / 2, height / 2));

            const link = svg.selectAll("line")
                .data(data.links)
                .enter().append("line")
                .style("stroke", "#999")
                .style("stroke-width", 2);

            const node = svg.selectAll("g")
                .data(data.nodes)
                .enter().append("g");

            node.append("image")
                .attr("xlink:href", d => d.image)
                .attr("width", 50)
                .attr("height", 50)
                .attr("x", -25)
                .attr("y", -25);

            node.append("text")
                .attr("dy", -30)
                .attr("text-anchor", "middle")
                .text(d => d.name);

            simulation.on("tick", () => {
                link.attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node.attr("transform", d => `translate(${d.x},${d.y})`);
            });
        });
});
