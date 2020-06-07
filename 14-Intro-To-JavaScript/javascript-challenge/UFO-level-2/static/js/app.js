// link var data from data.js to this app.js file.
const tableData = data;
const tbody = d3.select("tbody");
const filterTableButton = d3.select("#filter-btn");

// Show all data at first
tableData.forEach(ufoData => {
    var row = tbody.append("tr");
    Object.entries(ufoData).forEach(([key, value]) => {
      var cell = row.append("td");
      cell.text(value);
    });
});

// Create a function that can filter table data
function filterTableData() {

  var fiterDate = d3.select("#datetime").property("value");
  var cityName = d3.select("#city").property("value");
  var stateName = d3.select("#state").property("value");
  var countryName = d3.select("#country").property("value");
  var shapeName = d3.select("#shape").property("value");

  // remove any children tag from the <tbody>
  // https://www.w3schools.com/jsref/met_node_removechild.asp
  var list = document.getElementById("tbodyID");
  while (list.hasChildNodes()) {  
    list.removeChild(list.firstChild);
  }

  // insert tableData one by one
  tableData.forEach(ufoData => {

    console.log(ufoData["datetime"])

    if (ufoData["datetime"] === fiterDate &&
        ufoData['city'] === cityName &&
        ufoData['state'] === stateName &&
        ufoData['country'] === countryName &&
        ufoData['shape'] === shapeName
       )
    {
      var row = tbody.append("tr");
      Object.entries(ufoData).forEach(([key, value]) => {
      var cell = row.append("td");
      cell.text(value);
      });
    };
  });

  console.log(fiterDate, " Completed.");
};



