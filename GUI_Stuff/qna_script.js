document.getElementById('runButton').addEventListener('click', () => {
    const code = document.getElementById('code').value;
    const outputBox = document.getElementById('outputBox');

    //simulating the execution of code.
    try {
        const result = eval(code);
        outputBox.textContent = result !== undefined ? result : 'Code executed successfully.';
    } catch (error) {
        outputBox.textContent = 'Error: ' + error.message;
    }
});
