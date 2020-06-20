// init
const numOtuDisplay = 10;

let globalSampleData;

d3.json("./data/samples.json").then(function(data) {

    // Save JSON data to a global variable
    globalSampleData = data;

    // Create a list of individual IDs as Dropdown options (Week 16-1 material)
    var individualID = data.names;

	d3.select("select")
	    .selectAll("option")
		.data(individualID)
        .enter()
        .append("option")
		.text(function(d) { return d; })
        .attr("value", function (d) {return d;});

    // Create default bar char
    let defaultData = data.samples[0];
    let sampleValues = defaultData.sample_values.slice(0, numOtuDisplay);
    let otuIds = defaultData.otu_ids
                    .slice(0, numOtuDisplay)
                    .map(itm => "OTU " + itm.toString() + "  ");

    let otuLabels = defaultData.otu_labels.slice(0, numOtuDisplay)

    var tracer = {
        x : sampleValues.reverse(),
        y : otuIds.reverse(),
        text : otuLabels.reverse(),
        type : "bar",
        orientation: 'h'
    };

    var layout = {
        title : `Sample ${data.samples[0].id} Top 10 OTU`,
      };

    var barData = [tracer];
    Plotly.newPlot('bar', barData, layout);

    // Create default bubble chart
    var bubbleTracer = {
        x: defaultData.otu_ids,
        y: defaultData.sample_values,
        mode: 'markers',
        marker: {
          size: defaultData.sample_values,
          color : defaultData.otu_ids
        }
      };
      
      var bubbleData = [bubbleTracer];
      
      var bubleLayout = {
        title : `Sample Bubble Chart`,
        showlegend : false,
        height : 600,
        width : 1200
      };
      
      Plotly.newPlot("bubble", bubbleData, bubleLayout);

    // Create default metadata
    demographicInfo = data.metadata[0];
    d3.select("#sample-metadata").insert("ul");
    d3.select("ul").selectAll("li")
    .data(demographicInfo)
    .append("li")
    .text(function(d) {
      return d;
    });

    console.log(demographicInfo);
});

function optionChanged() {
    // Use D3 to select the dropdown menu
    var dropdownMenu = d3.select("#selDataset");
    // Assign the value of the dropdown menu option to a variable
    var testSubjectID = dropdownMenu.property("value");
    console.log(`Looking for Test Subject ${testSubjectID} data...`);

    // Find Test Subject's index from the Sample Data
    var idx = 0;
    for (i = 0; i < globalSampleData.names.length; i++) {
        if (globalSampleData.names[i] === testSubjectID) {
            idx = i;
            break;
        }
      }
    console.log(`Test Subject ${testSubjectID} is ${idx} on the list.`);
  
    // Update Bar Chart
    updateBarChart(idx, testSubjectID);

    // Update Bubble Chart
    updateBubbleChart(idx, testSubjectID);
};

function updateBarChart(idx, testSubjectID) {
    // 2. Create a horizontal bar chart with a dropdown menu to display the top 10 OTUs found in that individual.

    // Test Subject Sample Data
    var testSubjectSample = globalSampleData.samples[idx];
    // * Use `sample_values` as the values for the bar chart.
    var x = testSubjectSample.sample_values.slice(0, numOtuDisplay);
    // * Use `otu_ids` as the labels for the bar chart.
    var y = testSubjectSample.otu_ids.slice(0, numOtuDisplay).map(itm => "OTU " + itm.toString() + "  ");
    // * Use `otu_labels` as the hovertext for the chart.
    var text = testSubjectSample.otu_labels.slice(0, numOtuDisplay);
    
    // Update an exsiting bar chart
    Plotly.restyle("bar", "x", [x.reverse()]);
    Plotly.restyle("bar", "y", [y.reverse()]);
    Plotly.restyle("bar", "text", [text.reverse()]);
    
    // Update Chart Title
    var update = {
        title: `Sample ${testSubjectID} Top 10 OTU`, // updates the title
    };
    Plotly.relayout("bar", update);
}

function updateBubbleChart(idx, testSubjectID) {
    // 3. Create a bubble chart that displays each sample.

    // Test Subject Sample Data
    var testSubjectSample = globalSampleData.samples[idx];

    // * Use `otu_ids` for the x values.
    // * Use `sample_values` for the y values.
    // * Use `sample_values` for the marker size.
    // * Use `otu_ids` for the marker colors.
    // * Use `otu_labels` for the text values.

    var bubbleTracer = {
        x: testSubjectSample.otu_ids,
        y: testSubjectSample.sample_values,
        mode: 'markers',
        marker: {
          size: testSubjectSample.sample_values,
          color : testSubjectSample.otu_ids
        }
      };
      
      var bubbleData = [bubbleTracer];
      
      var bubleLayout = {
        title : `Sample Bubble Chart`,
        showlegend : false,
        height : 600,
        width : 1200
      };
      
      Plotly.newPlot("bubble", bubbleData, bubleLayout);

}


// 4. Display the sample metadata, i.e., an individual's demographic information.

// 5. Display each key-value pair from the metadata JSON object somewhere on the page.

// ![hw](Images/hw03.png)

// 6. Update all of the plots any time that a new sample is selected.

// Additionally, you are welcome to create any layout that you would like for your dashboard. An example dashboard is shown below:

// ![hw](Images/hw02.png)