// keplr.js


async function getKeplrAccount() {
  if (!window.keplr) {
    alert("Please install keplr extension");
  } else {
    const chainId = "injective-888";

    await window.keplr.enable(chainId);
    // Get the offline signer for your
    const offlineSigner = window.keplr.getOfflineSigner(chainId);

    // Get the user's accounts
    const accounts = await offlineSigner.getAccounts();
    console.log(accounts);

    // Check if the address is already stored in local storage
    const address = localStorage.getItem('address');

    // If the address is not stored in local storage, post it to the server
    if (!address) {
      postKeplrAccounts(accounts);
    }

    // This can let you know the Keplr is installed and the user is logged in to the Keplr
    return accounts[0]; // Returns the first account address
  }
}

async function postKeplrAccounts(accounts) {

  // Create a new HTTP request
  const request = new XMLHttpRequest();

  // Set the request method and URL
  request.open("POST", "https://data-storage-bu6vz2kbtq-uc.a.run.app/saveAddress");

  // Set the request header
  request.setRequestHeader("Content-Type", "application/json");

  // Create data
  const data = {
    wallet_address: {
      address: accounts[0].address,
    },
  };

  // Store in local cache
  localStorage.setItem('address', accounts[0].address);

  // Send the request
  request.send(JSON.stringify(data));
}
