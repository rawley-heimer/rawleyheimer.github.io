/* Adds a "Copy BibTeX" button under each BibTeX block. The page works without it. */
document.querySelectorAll('pre[data-bib]').forEach(function (pre) {
  if (!navigator.clipboard) return;
  var b = document.createElement('button');
  b.type = 'button'; b.className = 'copy'; b.textContent = 'Copy BibTeX';
  b.addEventListener('click', function () {
    navigator.clipboard.writeText(pre.textContent).then(function () {
      b.textContent = 'Copied';
      setTimeout(function () { b.textContent = 'Copy BibTeX'; }, 1600);
    });
  });
  pre.parentNode.insertBefore(b, pre.nextSibling);
});
