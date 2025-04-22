//Function to scross to the top
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

//Function to show/hide for iframe
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
          position: 'bottom',
          align: 'start',
          labels: {
          textAlign: 'left',
          boxWidth: 30,
          padding: 10,
          font: {
            size: 10
          }
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


//Function to trust factor and security breach pie chart 
Chart.register(ChartDataLabels);

window.addEventListener('DOMContentLoaded', function () {
  const trustFactorCtx = document.getElementById('trustFactorChart').getContext('2d');
  const breachCtx = document.getElementById('securityBreachChart').getContext('2d');

  // Chart 1: Trust Factor (Pie)
  new Chart(trustFactorCtx, {
    type: 'doughnut',
    data: {
      labels: ["1", "2", "3", "4", "5"],
      datasets: [{
        data: [30, 25, 27, 10, 8],
        backgroundColor: ["#4F81BD", "#C0504D", "#9BBB59", "#8064A2", "#00B0F0"]
      }]
    },
    options: {
      responsive: true,
      cutout: '0%',
      radius: '80%', 
      plugins: {
        datalabels: {
          formatter: (value) => `${value}%`,
          color: "#fff",
          font: {
            weight: 'bold',
            size: 14
          }
        },
        legend: {
          display: false
        }
      }
    },
    plugins: [ChartDataLabels]
  });

  // Chart 2: Knowledge About Security Breach (Donut)
  new Chart(breachCtx, {
    type: 'doughnut',
    data: {
      labels: ["No", "Not Sure", "Yes"],
      datasets: [{
        data: [40, 30, 30],
        backgroundColor: ["#4F81BD", "#C0504D", "#9BBB59"]
      }]
    },
    options: {
      responsive: true,
      cutout: '50%',
      plugins: {
        datalabels: {
          formatter: (value) => `${value}%`,
          color: "#fff",
          font: {
            weight: 'bold',
            size: 14
          }
        },
        legend: {
          position: 'bottom',
          labels: {
            font: {
              size: 13
            }
          }
        }
      }
    },
    plugins: [ChartDataLabels]
  });
});
