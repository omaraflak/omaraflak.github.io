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
const headerElement = document.getElementById('header');
if (headerElement) {
  fetch('../header.html')
    .then(response => response.text())
    .then(html => {
      headerElement.innerHTML = html;
    });
}

// Load footer.html into #footer if the element exists
const footerElement = document.getElementById('footer');
if (footerElement) {
  fetch('../footer.html')
    .then(response => response.text())
    .then(html => {
      footerElement.innerHTML = html;
    });
} 