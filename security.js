function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
  
function toggleIframe() {
    const iframeContainer = document.getElementById("iframeContainer");
    const button = document.getElementById("toggleButton");

    if (iframeContainer.style.display === "none") {
      iframeContainer.style.display = "block";
      button.textContent = "Hide Survey Results";
    } else {
      iframeContainer.style.display = "none";
      button.textContent = "View Survey Results";
    }
  }

//Function for Pie Chatt for Familiarity With Cryptocurrency
window.addEventListener('DOMContentLoaded', function () {
  const ctx = document.getElementById('cryptoFamiliarityChart').getContext('2d');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: [
        "Cryptocurrency is the future of finance.",
        "I am concerned there are too many scams",
        "I avoid them because I don’t trust the system",
        "I don’t have any investment at the moment but will use them.",
        "I don’t use them because they are for techy people.",
        "Yes. I have already invested in them."
      ],
      datasets: [{
        label: 'Familiarity with Cryptocurrency',
        data: [15, 15, 20, 15, 12, 23],
        backgroundColor: [
          "#6baed6",
          "#de2d26",
          "#74c476",
          "#9e9ac8",
          "#a1d99b",
          "#fd8d3c"
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'right',
          labels: {
          boxWidth: 30,
          padding: 10,
          font: {
            size: 14
          }
        },
        title: {
          display: true,
          text: 'Familiarity with Cryptocurrency'
        }
      }
    }
  });
});
