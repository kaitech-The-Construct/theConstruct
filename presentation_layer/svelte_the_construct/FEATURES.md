# The Construct: Feature Prompts

This document outlines the features for "The Construct" decentralized robotics exchange. The features are organized by development phase, as detailed in the project roadmap. Each feature description is designed to serve as a detailed prompt for an LLM to generate the necessary Svelte components and logic.

## Architectural Approach

The application will be built using a modular, component-based architecture in Svelte. This ensures maintainability and scalability. Key principles include:
- **Componentization**: Each distinct piece of UI is a reusable component.
- **Centralized State Management**: Svelte stores (`src/lib/stores`) will manage shared application state like user session and wallet information.
- **Service Abstraction**: Logic for interacting with the XRPL (or other external services) will be abstracted into service modules (`src/lib/services`) to keep components clean and focused on the UI.
- **Routing**: Features will be organized under distinct routes (`src/routes`) to keep concerns separated.

---

## Phase 1: Minimal Viable Product (MVP) – Core Marketplace on XRPL

### 1. Basic Catalog of Robotics Components

**Description:**
Create a Svelte component to display a catalog of robotics components. The UI should be a responsive grid of product cards that showcases the items available for sale. This component will serve as the main entry point for users browsing the marketplace.

**LLM Prompt:**
"Create a feature for displaying a catalog of robotics products in a Svelte application.
1.  **Data Source:** Create a mock data file at `src/lib/data/products.json`. Each product object should have an `id`, `name`, `description`, `price`, `currency` (e.g., "XRP"), and `imageUrl`.
2.  **Component Structure:**
    *   `src/lib/components/product/ProductCard.svelte`: A reusable component to display a single product's image, name, and price.
    *   `src/lib/components/product/ProductGrid.svelte`: A component that fetches the data from `products.json` and renders a `ProductCard` for each item in a responsive grid layout.
3.  **Routing:** Create a new route at `src/routes/marketplace/+page.svelte` and display the `ProductGrid` component there.
4.  **Interaction:** Clicking on a `ProductCard` should navigate the user to a product detail page using the URL structure `/product/[id]`."

### 2. User Accounts & Wallet Integration

**Description:**
Implement a user authentication system based on XRPL wallet connectivity. This feature allows users to connect their existing wallets to the application to manage their identity and assets securely.

**LLM Prompt:**
"Create a user authentication feature for the Svelte app using an XRPL wallet.
1.  **State Management:** Create a Svelte store at `src/lib/stores/userStore.js` to manage the user's connection state (`isConnected`), wallet address (`address`), and balance.
2.  **XRPL Service:** Create a service module at `src/lib/services/xrplClient.js`. Initially, this service should contain mock functions for `connectWallet()` and `disconnectWallet()`. The `connectWallet()` function should simulate a successful connection and update the `userStore` with a mock address.
3.  **UI Components:**
    *   `src/lib/components/layout/Header.svelte`: Add a 'Connect Wallet' button to the application header.
    *   When disconnected, the button should say "Connect Wallet" and trigger the `connectWallet()` function on click.
    *   When connected, the button should display the truncated user wallet address and, when clicked, offer a "Disconnect" option that calls `disconnectWallet()`.
4.  **Global Access:** Ensure the header is part of the main layout (`src/routes/+layout.svelte`) so it is visible on all pages."

### 3. Core Purchasing & Product Detail View

**Description:**
Create a detailed view for a single product and implement the initial logic for purchasing an item using an XRPL transaction.

**LLM Prompt:**
"Create a dynamic product detail page and purchasing mechanism.
1.  **Routing:** Create a dynamic route at `src/routes/product/[id]/+page.svelte`.
2.  **Data Loading:** In the page's load function, retrieve the `id` from the URL parameters and use it to find and display the correct product details from `src/lib/data/products.json`.
3.  **UI:** The page must display the product's name, a gallery of images (using the single `imageUrl` for now), a full description, and its price.
4.  **Purchase Button:** Add a 'Buy Now' button. This button should be disabled if the user's wallet is not connected (check the `userStore`).
5.  **Transaction Logic:** When the 'Buy Now' button is clicked, it should call a new `createOffer()` function in the `xrplClient.js` service. This function should simulate creating an `OfferCreate` transaction on the XRPL and log the transaction details to the console. Provide UI feedback for the transaction's status (e.g., "Submitting...", "Success!", "Failed")."

### 4. Basic Smart Contract Escrow

**Description:**
Integrate XRPL's native escrow functionality into the purchase flow to ensure funds are held securely until the transaction is confirmed by both parties. This includes a user-facing page to manage orders.

**LLM Prompt:**
"Enhance the purchasing flow to use XRPL's native escrow and create an order management page.
1.  **Update XRPL Service:** In `src/lib/services/xrplClient.js`, replace the `createOffer()` function with three new mock functions: `createEscrow(productId, amount)`, `finishEscrow(orderId)`, and `cancelEscrow(orderId)`.
2.  **Update Purchase Flow:** When a user clicks 'Buy Now' on the product detail page, it should now call the `createEscrow()` function.
3.  **Order Management Page:**
    *   Create a new route at `src/routes/account/orders/+page.svelte`.
    *   Create a mock data file `src/lib/data/orders.json` with sample orders, each having an `id`, `productId`, `status` ('In Escrow', 'Completed', 'Canceled'), and `date`.
    *   The page should fetch and display a list of the user's orders.
4.  **Order Interaction:** For orders with the status 'In Escrow', display a 'Confirm Receipt' button. Clicking this button should call the `finishEscrow()` function with the order's ID and update the UI to reflect the 'Completed' status."

---

## Phase 2: Expanded Marketplace & Tokenization

### 1. Expanded Inventory & Listing Tools

**Description:**
Create a feature for approved sellers to list their own robotics components on the marketplace. This involves a form that captures product details and creates a new listing.

**LLM Prompt:**
"Create a feature that allows approved users to list new products for sale.
1.  **Route & Guarding:** Create a new route at `src/routes/account/listings/new/+page.svelte`. This page should be protected, for now, by checking if the user's connected wallet address is on a hardcoded list of approved sellers in `userStore.js`. If not, show an 'Access Denied' message.
2.  **Listing Form:** Create a `ProductListingForm.svelte` component in `src/lib/components/product/`. The form should have input fields for `name`, `description`, `price`, `currency`, and `imageUrl`.
3.  **Submission Logic:** On form submission, gather the data and call a new `listProduct()` function in `xrplClient.js`. This function will simulate creating the on-chain listing and, on success, should add the new product to the `products.json` file (for mock purposes) and redirect the user to their new product's detail page."

### 2. Ratings, Reviews, & Reputation System

**Description:**
Implement a system for buyers to rate and review sellers after a purchase is completed. Ratings will be displayed on product and seller pages to build trust.

**LLM Prompt:**
"Create a ratings and reviews feature.
1.  **Submission UI:** On the `account/orders` page, for any order with a 'Completed' status, display a 'Leave a Review' button. Clicking it should reveal a simple form with a 5-star rating input and a textarea for a text review.
2.  **Data Storage:** Create a `src/lib/data/reviews.json` file to store reviews, linking them by `productId` or `sellerId`.
3.  **Submission Logic:** On submission, the review data should be saved. In a real implementation, this would be recorded as a memo in an XRPL transaction. For now, just append it to the `reviews.json` file.
4.  **Display Reviews:** On the `product/[id]` page, fetch and display all reviews associated with that product. Show the average star rating at the top and a list of individual reviews at the bottom."

---

## Phase 3: Advanced Features & Ecosystem Growth

### 1. Decentralized Governance

**Description:**
Introduce a governance system where token holders can vote on platform proposals. This feature fosters community-driven development and decision-making.

**LLM Prompt:**
"Create a decentralized governance feature.
1.  **Data:** Create a `src/lib/data/proposals.json` file with a list of governance proposals. Each should have an `id`, `title`, `description`, `status` ('Active', 'Passed', 'Failed'), and vote counts (`for`, `against`).
2.  **Proposal List Page:** Create a route at `src/routes/governance/+page.svelte` that displays a list of all proposals.
3.  **Proposal Detail Page:** Create a dynamic route at `src/routes/governance/[id]/+page.svelte`. This page should show the full proposal details and the current voting results.
4.  **Voting UI:** On the detail page for an 'Active' proposal, display 'Vote For' and 'Vote Against' buttons.
5.  **Voting Logic:** Clicking a vote button should call a `castVote(proposalId, vote)` function in `xrplClient.js`. This function should simulate submitting the vote via an XRPL transaction and update the vote counts in the `proposals.json` file for the mock-up."
