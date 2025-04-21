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
