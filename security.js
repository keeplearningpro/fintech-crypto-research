function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showIframe() {
    const iframeContainer = document.getElementById('iframeContainer');
    const iframe = document.getElementById('surveyFrame');

    Using Google Docs Viewer to read excel in frame
    const fileUrl = "https://keeplearningpro.github.io/fintech-crypto-research/data/survey.xlsx";
    const gviewUrl = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(fileUrl);

    iframe.src = gviewUrl;
    iframeContainer.style.display = 'block';
  }
