// KaTeX auto-render
if (typeof renderMathInElement === 'function') {
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$", right: "$", display: false },
      { left: "$$", right: "$$", display: true },
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true }
    ]
  });
}

// Load header.html into #header if the element exists
const headerEl = document.getElementById('header');
if (headerEl) {
  fetch('../header.html')
    .then(response => response.text())
    .then(html => {
      headerEl.innerHTML = html;
    });
} 