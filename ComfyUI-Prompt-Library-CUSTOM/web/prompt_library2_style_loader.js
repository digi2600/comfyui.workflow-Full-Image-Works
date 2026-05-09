// Auto-inject the CSS stylesheet for Prompt Library
(function () {
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = new URL("./prompt_library2.css", import.meta.url).href;
  document.head.appendChild(link);
})();
