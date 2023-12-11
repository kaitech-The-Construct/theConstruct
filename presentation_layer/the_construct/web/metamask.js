// metamask.js

// You should check if the user has MetaMask installed
if (typeof window.ethereum !== 'undefined') {
    console.log('MetaMask is installed!');
  }
  
  async function getAccount() {
    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
    return accounts[0]; // Returns the first account
  }