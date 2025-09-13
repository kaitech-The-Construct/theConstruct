# The Construct - Svelte Frontend

## Overview

The Construct is a decentralized robotics exchange (DREX) built with **SvelteKit** that democratizes and streamlines the robotics industry. This frontend application provides a secure, efficient, and transparent marketplace interface using a hybrid blockchain approach with XRPL and Solana integration.

## 🚀 Tech Stack

- **Framework**: SvelteKit 2.x with TypeScript
- **Styling**: Tailwind CSS 4.x + DaisyUI 5.x
- **Build Tool**: Vite 7.x
- **Testing**: Vitest + Testing Library
- **Blockchain**: XRPL 4.x
- **HTTP Client**: Axios
- **Real-time**: Socket.io Client
- **Charts**: Chart.js 4.x

## ✨ Key Features

### Core Marketplace
- **Decentralized Trading**: Hybrid XRPL/Solana blockchain integration
- **Product Catalog**: Responsive grid of robotics components and kits
- **Secure Escrow**: XRPL native escrow with Solana smart contract enhancements
- **Multi-Chain Wallets**: Support for both XRPL and Solana wallet connections

### User Experience
- **Modern UI**: Clean, responsive design with Tailwind CSS and DaisyUI
- **Real-Time Updates**: Live notifications and status updates via WebSocket
- **TypeScript**: Full type safety throughout the application
- **Component Architecture**: Modular, reusable Svelte components

### Advanced Features
- **Tokenization**: Digital tokens representing physical robotics assets
- **Reputation System**: Community-driven ratings and reviews
- **Governance**: Decentralized voting on platform proposals
- **Analytics**: Interactive charts and data visualization

## 🛠 Development Setup

### Prerequisites
- Node.js 18+ 
- Yarn package manager
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/kaitech-corp/theConstruct.git
cd theConstruct/presentation_layer/svelte_the_construct

# Install dependencies
yarn install

# Start development server
yarn dev
```

### Available Scripts

```bash
# Development
yarn dev              # Start dev server with hot reload
yarn preview          # Preview production build locally

# Building
yarn build            # Build for production

# Code Quality
yarn check            # Run Svelte type checking
yarn check:watch      # Run type checking in watch mode
yarn lint             # Run ESLint and Prettier checks
yarn format           # Format code with Prettier

# Testing
yarn test             # Run unit tests
yarn test:ui          # Run tests with UI interface
```

## 📁 Project Structure

```
src/
├── lib/
│   ├── components/     # Reusable Svelte components
│   │   ├── layout/     # Header, Footer, Navigation
│   │   ├── product/    # ProductCard, ProductGrid, etc.
│   │   └── ui/         # Buttons, Forms, Modals
│   ├── stores/         # Svelte stores for state management
│   │   ├── userStore.js    # User authentication & wallet
│   │   └── appStore.js     # Global application state
│   ├── services/       # Blockchain and API services
│   │   ├── xrplClient.js   # XRPL integration
│   │   ├── solanaClient.js # Solana integration
│   │   └── api.js          # HTTP API client
│   └── data/          # Mock data and constants
├── routes/            # SvelteKit file-based routing
│   ├── marketplace/   # Product catalog and listings
│   ├── product/       # Product detail pages
│   ├── account/       # User dashboard and orders
│   └── governance/    # DAO voting and proposals
├── app.css           # Global styles
└── app.html          # HTML template
```

## 🔗 Blockchain Integration

### XRPL Features
- **Fast Transactions**: Low-cost, rapid settlement for trading
- **Native Escrow**: Built-in escrow functionality for secure transactions
- **Token Issuance**: Represent physical robotics components as digital assets
- **Wallet Integration**: Seamless connection with XRPL-compatible wallets

### Solana Features
- **Smart Contracts**: Advanced business logic and conditional transactions
- **Governance**: Decentralized voting and proposal mechanisms
- **Complex Orders**: Multi-party agreements and sophisticated trading features
- **Reputation System**: On-chain reputation tracking and community trust

## 🎯 Development Roadmap

### Phase 1: MVP (Current)
- [x] Basic product catalog with responsive design
- [x] XRPL/Solana wallet integration
- [x] Core purchasing flow with escrow
- [x] Order management system

### Phase 2: Expanded Marketplace
- [ ] Seller listing tools and inventory management
- [ ] Ratings and reviews system
- [ ] Advanced search and filtering
- [ ] Multi-currency support

### Phase 3: Advanced Ecosystem
- [ ] Decentralized governance interface
- [ ] Analytics dashboard with Chart.js
- [ ] IoT device integration
- [ ] Community features and social trading

## 🧪 Testing

The project uses Vitest for unit testing with Testing Library for component testing:

```bash
# Run all tests
yarn test

# Run tests with coverage
yarn test --coverage

# Run tests in UI mode
yarn test:ui
```

## 🚀 Deployment

### Production Build
```bash
yarn build
```

The built application will be in the `build/` directory, ready for deployment to any static hosting service or Node.js server.

### Environment Variables
Create a `.env` file in the project root:

```env
VITE_XRPL_SERVER=wss://xrplcluster.com
VITE_SOLANA_RPC=https://api.mainnet-beta.solana.com
VITE_API_BASE_URL=https://api.theconstruct.exchange
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## 🆘 Support and Feedback

If you have any questions, encounter issues, or would like to provide feedback, please reach out to our support team at [Randy@kaitechcorp.com](mailto:Randy@kaitechcorp.com).

## 🔗 Related Documentation

- [FEATURES.md](svelte_the_construct/FEATURES.md) - Detailed feature specifications
- [OVERVIEW.md](svelte_the_construct/OVERVIEW.md) - Project vision and architecture
- [ROADMAP.md](svelte_the_construct/ROADMAP.md) - Development timeline and milestones
