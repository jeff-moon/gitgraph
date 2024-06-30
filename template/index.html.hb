<!DOCTYPE html>
<html>
  <head>
    <script>
      window.onload = function () {
        var chart = new CanvasJS.Chart("chartContainer", {
          animationEnabled: false,
          zoomEnabled: true,
          toolTip: {
            content: "{x}: {hash}: {y} lines",
          },
          title: {
            text: "Total SLOC",
          },
          axisX: {
            valueFormatString: "YYYY DD MMM",
          },
          axisY: {
            title: "SLOC Count",
          },
          data: [
            {
              name: "Data",
              type: "line",
              showInLegend: true,
              xValueFormatString: "YYYY DD MMM",
              color: "#F08080",
              dataPoints: [
                {{#each commits}}
                {
                  x: new Date("{{x}}"),
                  y: {{y}},
                  hash: "{{hash}}",
                  desc: "{{desc}}"
                },
                {{/each}}
              ],
            },
            {{#if plan}}
            {
              name: "Plan",
              type: "line",
              showInLegend: true,
              axisYType: "secondary",
              color: "#00FF00",
              dataPoints: [
                {{#each plan}}
                {
                  x: new Date("{{x}}"),
                  y: {{y}},
                  hash: "PLAN",
                  desc: ""
                },
                {{/each}}
              ],
            },
            {{/if}}
          ],
        });
        chart.render();
      };
    </script>
  </head>
  <body>
    <div id="chartContainer" style="height: 300px; width: 800px"></div>
    <script src="canvasjs.min.js"></script>
  </body>
</html>
