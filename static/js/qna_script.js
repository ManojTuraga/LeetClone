document.getElementById('runButton').addEventListener('click', () => {
    const code = document.getElementById('code').value;
    fetch( "/qna", {
      method: "POST",
      data: code  
    } )

});
