// keplr.js

async function getKeplrAccount(chainId) {
    if (!window.getOfflineSigner || !window.keplr) {
      throw new Error('Please install Keplr extension');
    }
  
    // Enabling before using Keplr's API
    await window.keplr.enable(chainId);
  
    const offlineSigner = window.getOfflineSigner(chainId);
    const accounts = await offlineSigner.getAccounts();
  
    // This can let you know the Keplr is installed and the user is logged in to the Keplr
    return accounts[0].address; // Returns the first account address
  }