/* Copy the visible example without changing its whitespace or contents. */
document.querySelectorAll('pre > code').forEach((code, index) => {
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy-button';
  button.textContent = 'Copy code';
  button.setAttribute('aria-label', `Copy code block ${index + 1}`);
  code.parentElement.before(button);
  button.addEventListener('click', async () => {
    const status = document.getElementById('copy-status');
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = 'Copied';
      status.textContent = 'Code copied. Paste it into the terminal or file named by the exercise.';
      window.setTimeout(() => { button.textContent = 'Copy code'; }, 2000);
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Code selected. Use your browser\'s Copy command.';
    }
  });
});
