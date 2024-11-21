document.addEventListener('DOMContentLoaded', () => {
    const joinButton = document.getElementById('join-button');
    const generateButton = document.getElementById('generate-button');
    const startButton = document.getElementById('start-button');
    const waitingRoomList = document.getElementById('waiting-room-list');
    const generatedCodeElement = document.getElementById('generated-code');
    
    let players = [];
    let currentPartyCode = '';
  
    // Handle Join Party
    joinButton.addEventListener('click', () => {
      const codeInput = document.getElementById('join-code').value;
      if (codeInput === currentPartyCode) {
        players.push(`Player ${players.length + 1}`);
        updateWaitingRoom();
        alert('Successfully joined the party!');
      } else {
        alert('Invalid code!');
      }
    });
  
    // Handle Generate Code
    generateButton.addEventListener('click', () => {
      currentPartyCode = generateRandomCode();
      generatedCodeElement.textContent = `Party Code: ${currentPartyCode}`;
    });
  
    // Handle Start Party
    startButton.addEventListener('click', () => {
      if (players.length > 0) {
        alert('Party started!');
        //trigger further actions like redirecting to a new page here.
      } else {
        alert('No players have joined yet.');
      }
    });
  
    // Update the waiting room list
    function updateWaitingRoom() {
      waitingRoomList.innerHTML = '';
      players.forEach(player => {
        const listItem = document.createElement('li');
        listItem.textContent = player;
        waitingRoomList.appendChild(listItem);
      });
    }
  
    // Generate random 6-digit code
    function generateRandomCode() {
      return Math.floor(100000 + Math.random() * 900000).toString();
    }
  });
  