// Reusable function to create a card
function createDesignCard(item) {
  const num = Math.floor(Math.random() * 5);
  const card = document.createElement("div");
  card.className = "card";

  const cardImage = document.createElement("img");
  cardImage.src = item.url_to_images[num];
  cardImage.alt = "Design image";
  cardImage.className = "card-image";
  card.appendChild(cardImage);

  const cardTitle = document.createElement("h2");
  cardTitle.className = "card-title";
  cardTitle.textContent = item.designer;
  card.appendChild(cardTitle);

  const cardTextStatus = document.createElement("p");
  cardTextStatus.className = "card-text";
  cardTextStatus.textContent = `Status: ${item.current_status}`;
  card.appendChild(cardTextStatus);

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
    title.textContent = item.designer;

    // Create a text element for the modal
    const category = document.createElement("p");
    category.textContent = item.category;

    // Create a text element for the modal
    const description = document.createElement("p");
    description.textContent = item.additional_info.note;

    // Create a text element for the modal
    const specifications = document.createElement("p");
    specifications.textContent = `
        Height: ${item.specifications.dimensions.height} \n
        Width: ${item.specifications.dimensions.width} \n
        Weight: ${item.specifications.weight} \n
        Materials: ${item.specifications.materials} \n`;

    // Create a text element for the modal
    const status = document.createElement("p");
    status.textContent = `Status: ${item.current_status}`;



    // Append elements to modalTextContent
    modalTextContent.appendChild(modalCloseButton);
    modalTextContent.appendChild(title);
    modalTextContent.appendChild(category);
    modalTextContent.appendChild(description);
    modalTextContent.appendChild(status);
    modalTextContent.appendChild(specifications);

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
  const designList = document.getElementById("product-list-design");
  const apiUrl =
    "https://application-layer-bu6vz2kbtq-uc.a.run.app/design/list";

  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      data.forEach((item) => {
        const card = createDesignCard(item);
        designList.appendChild(card);
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
});
