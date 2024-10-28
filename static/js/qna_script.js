document.getElementById('runButton').addEventListener('click', () => {
  const code = document.getElementById('code').value;
  fetch("/qna", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ code: code })
  });
});
