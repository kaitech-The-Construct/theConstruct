// Reusable function to create a card
function createRobotCard(item) {
  const card = document.createElement("div");
  card.className = "card";

  const cardImage = document.createElement("img");
  cardImage.src = item.image_url;
  cardImage.alt = "Robot image";
  cardImage.className = "card-image";
  card.appendChild(cardImage);

  const cardTitle = document.createElement("h2");
  cardTitle.className = "card-title";
  cardTitle.textContent = item.model;
  card.appendChild(cardTitle);

  const cardText = document.createElement("p");
  cardText.className = "card-text";
  cardText.textContent = item.manufacturer;
  card.appendChild(cardText);

  const cardActions = document.createElement("div");
  cardActions.className = "card-actions";

  const addToCartLink = document.createElement("a");
  addToCartLink.href = "#";
  addToCartLink.textContent = "Add to Cart";
  cardActions.appendChild(addToCartLink);

  card.appendChild(cardActions);

  // Add click event to open a modal
  card.addEventListener("click", () => {
    // Create the modal container
    const modalContainer = document.createElement("div");
    modalContainer.className = "modal-container";

    // Create the modal itself
    const modal = document.createElement("div");
    modal.className = "modal";

    // Create modal close button
    const modalCloseButton = document.createElement("button");
    modalCloseButton.className = "modal-close-button";

    modalCloseButton.addEventListener("click", () => {
      // Close the modal
      modal.style.display = "none";
    });

    // Create the modal content
    const modalContent = document.createElement("div");
    modalContent.className = "modal-content";

    // Create the modal text content
    const modalTextContent = document.createElement("div");
    modalTextContent.className = "modal-text-content";

    // Create the image for the modal
    const image = document.createElement("img");
    image.src = card.querySelector(".card-image").src;
    image.className = "modal-image";

    // Create a title for the modal
    const title = document.createElement("h2");
    title.textContent = card.querySelector(".card-title").textContent;

    // Create a text element for the modal
    const text = document.createElement("p");
    text.textContent = card.querySelector(".card-text").textContent;

    // Create a text element for the modal
    const description = document.createElement("p");
    text.textContent = item.description;

    // Create a price element for the modal
    const price = document.createElement("p");
    price.textContent = `Price: `;

    // Create a mapping of cryptocurrencies to prices
    const cryptoPrices = {
      "ETH": 0.00016,
      "INJ": 0.01,
      "SOL": 0.027,
    };

    // Create a select element for the cryptocurrencies
    const select = document.createElement("select");
    Object.keys(cryptoPrices).forEach((cryptocurrency) => {
      const option = document.createElement("option");
      option.value = cryptocurrency;
      option.textContent = cryptocurrency;
      select.appendChild(option);
    });

    // Add an event listener to the select element
    select.addEventListener("change", () => {
      // Get the selected cryptocurrency
      const selectedCrypto = select.value;

      // Update the price element with the corresponding price from the mapping
      price.textContent = `Price: ${cryptoPrices[selectedCrypto]}`;
    });

    // Append elements to modalTextContent
    modalTextContent.appendChild(modalCloseButton);
    modalTextContent.appendChild(title);
    modalTextContent.appendChild(text);
    modalTextContent.appendChild(description);
    modalTextContent.appendChild(price);
    modalTextContent.appendChild(select);

    // Append image and modalTextContent to modalContent
    modalContent.appendChild(image);
    modalContent.appendChild(modalTextContent);

    // Append modalContent to modal
    modal.appendChild(modalContent);

    // Append modal to the modal container
    modalContainer.appendChild(modal);

    // Append the modal container to the body of the document
    document.body.appendChild(modalContainer);

    // Show the modal
    // Show the modal and allow clicks on it
    modalContainer.style.display = "block";
    modal.style.pointerEvents = "auto";

    // Add a click event listener to close the modal when clicking outside of it
    document.addEventListener("click", function (event) {
      if (modal.style.display === "block") {
        if (event.target !== modal && event.target.closest(".modal") === null) {
          // Hide the modal and prevent clicks on it
          modal.style.display = "none";
          modal.style.pointerEvents = "none";
        }
      }
    });
  });

  return card;
}

// JavaScript to fetch data from the API and create cards
document.addEventListener("DOMContentLoaded", function () {
  const robotList = document.getElementById("product-list-robots");
  const apiUrl =
    "https://application-layer-bu6vz2kbtq-uc.a.run.app/robots/list";

  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      data.forEach((item) => {
        const card = createRobotCard(item);
        robotList.appendChild(card);
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
});
