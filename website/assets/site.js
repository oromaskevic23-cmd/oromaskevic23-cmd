/* Native links work without JavaScript. This only improves the language menu. */
for (const menu of document.querySelectorAll('.language-menu')) {
  document.addEventListener('click', event => { if (!menu.contains(event.target)) menu.open = false; });
  menu.addEventListener('keydown', event => {
    if (event.key === 'Escape') { menu.open = false; menu.querySelector('summary').focus(); }
  });
}
