const loadFileInElement = (fileLocation, elementId) => {
  const element = document.getElementById(elementId);
  if (element) {
    fetch(fileLocation)
      .then(response => response.text())
      .then(html => {
        element.innerHTML = html;
      });
  }
}
