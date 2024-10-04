//compare.js

document.addEventListener('DOMContentLoaded', function() {
  var compareButton = document.getElementById('compareButton');
  compareButton.addEventListener('click', function() {
    comparePrices();
  });
});

function comparePrices() {
  chrome.storage.local.get(['amazonProductTitles', 'amazonProductPrices'], function (result) {
    let amazonProductTitles = result.amazonProductTitles;
    let amazonProductPrices = result.amazonProductPrices;

    // Filter out any empty product titles
    amazonProductTitles = amazonProductTitles.filter(title => title.trim() !== "");

    if (!amazonProductTitles.length || !amazonProductPrices.length) {
      alert('Amazon product data is not available. Please set the product title and price.');
      return;
    }

    console.log({
      amazon_product_title: amazonProductTitles,
      amazon_product_price: amazonProductPrices
    });

    fetch('http://localhost:5010/compare', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amazon_product_title: amazonProductTitles,
        amazon_product_price: amazonProductPrices
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); // Log the response to check what data you are getting
      displayComparison(data);
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while fetching data. Please try again later.');
    });
  });
}



function displayComparison(data) {
  var resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = ""; // Clear previous results

  var flipkartPrices = data.flipkart_prices || [];
  var amazonPrices = data.amazon_prices || [];
  var comparisonResults = data.comparison_results || [];

  // Check if there's valid data
  if (flipkartPrices.length === 0 || amazonPrices.length === 0 || comparisonResults.length === 0) {
    alert("No data available for comparison.");
    return;
  }

  // Create and display Amazon result
  var amazonResult = document.createElement("div");
  amazonResult.classList.add("result");
  amazonResult.innerHTML = "<h3>Amazon</h3><p>" + amazonPrices[0] + "</p>";
  resultsDiv.appendChild(amazonResult);

  // Create and display Flipkart result
  var flipkartResult = document.createElement("div");
  flipkartResult.classList.add("result");
  flipkartResult.innerHTML = "<h3>Flipkart</h3><p>" + flipkartPrices[0] + "</p>";
  resultsDiv.appendChild(flipkartResult);

  // Create and display price difference
  var priceDifference = document.createElement("div");
  priceDifference.classList.add("result");
  var difference = Math.abs(parseFloat(amazonPrices[0]) - parseFloat(flipkartPrices[0])); 
  priceDifference.innerHTML = "<h3>Price Difference</h3><p>" + difference + "</p>";
  resultsDiv.appendChild(priceDifference);

  // Create and display comparison result
  var comparisonMessage = document.createElement("div");
  comparisonMessage.classList.add("result");
  comparisonMessage.innerHTML = "<h3 class='compare'>Comparison Result</h3><p>" + comparisonResults[0] + "</p>";
  resultsDiv.appendChild(comparisonMessage);
}
