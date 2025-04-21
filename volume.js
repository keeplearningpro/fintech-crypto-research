function showBlock(id, btn) {
      const block = document.getElementById(id);
      block.classList.remove('hidden');
      btn.style.display = 'none';
    }
    function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
