# The Construct — Decentralized Robotics Exchange (DREX) Frontend

A Flutter application for The Construct, a decentralized marketplace for robotics components, kits, and designs. It prioritizes XRPL (XRP Ledger) for fast, low-cost settlement and escrow, with a long-term vision to support hybrid workflows and advanced features.

- Project overview: docs/OVERVIEW.md
- Product roadmap: docs/ROADMAP.md

## Key Capabilities

- Marketplace UI: Browse curated robotics components and kits with structured metadata
- Auth: Firebase Authentication (Google, Apple) with Firebase Core/Analytics/Crashlytics
- Data: Firebase Firestore and Storage integrations
- State management: BLoC (bloc, flutter_bloc, equatable)
- Navigation: GoRouter with builder support (go_router_builder)
- Responsive UI: Responsive Framework, custom SizeConfig, theming
- Wallet/Web3 integration: Web helpers (web/metamask.js, web/keplr.js) and Flutter web3 packages for experimental/prototype features
- Search and discovery: Search screens/components for catalog navigation

See docs/OVERVIEW.md for the strategic context and docs/ROADMAP.md for phased delivery focusing on XRPL-first functionality.

## Tech Stack

- Flutter (mobile, web, desktop-ready)
- Firebase (Auth, Firestore, Storage, Analytics, Crashlytics, optional Functions)
- BLoC pattern for app state
- GoRouter for declarative routing
- Freezed + json_serializable for immutable models and code generation
- Responsive UI (responsive_framework, size config utilities)
- Prototype Web3 support via web3dart/flutter_web3 for EVM-style wallets; XRPL is the targeted ledger per roadmap

## Project Structure

- lib/main.dart: App bootstrap and router/theme wiring
- lib/services/project_initializer.dart: Flutter binding, URL strategy (web), Firebase initialization
- lib/services/navigation/: GoRouter config and navigation helpers
- lib/bloc/: BLoC state management (auth, login, generics, observer)
- lib/models/: Freezed models (e.g., robot_catalog, software_repo)
- lib/repositories/: Data access abstractions
- lib/screens/:
  - home/: Landing/home and components
  - marketplace.dart/: Marketplace listing, details, and nav
  - search/: Search bar and results
  - user_profile.dart/: Profile screen
  - integration/: Integration-related screens (e.g., wallet)
  - menu/: Drawer/menu components
- lib/ui/: Theme, responsive helpers, text styles
- lib/services/api/: API functions and wallet connect helpers
- web/: Web-specific assets and helper scripts (metamask.js, keplr.js)
- assets/images/: App imagery (logo, launch screen, roles)
- docs/: OVERVIEW.md and ROADMAP.md

## Getting Started

Prerequisites:
- Flutter SDK (3.1.4+ Dart constraint is set; ensure you have a recent stable)
- Xcode (for iOS), CocoaPods, and an Apple developer account for device deploys
- Android Studio / SDK, Java 11+ for Android builds
- A Firebase project (web config already included for web; mobile platforms require native config files below)

Install dependencies:
```
flutter pub get
```

Generate code (models, router builders, etc.):
```
dart run build_runner build --delete-conflicting-outputs
```

Run on Web:
```
flutter run -d chrome
```

Run on Android:
```
flutter run -d android
```

Run on iOS (simulator):
```
flutter run -d ios
```

Tip: If you add or modify Freezed/json_serializable models or GoRouter annotations, rerun build_runner.

## Firebase Configuration

Web:
- The web Firebase config is embedded in lib/services/project_initializer.dart for kIsWeb.
- This is safe; Firebase web configs are public client-side identifiers (not secrets). Secure calls still require Firebase security rules and server-side enforcement where applicable.

Android:
- Add google-services.json to android/app/
- Ensure the Gradle plugins are set (this repo already includes Firebase dependencies)

iOS:
- Add GoogleService-Info.plist to ios/Runner/
- Open ios/Runner.xcworkspace in Xcode for signing if deploying to device/TestFlight

Security rules:
- Set appropriate Firestore/Storage rules for your environment. Do not assume open access.

## Environment Notes

- URL strategy for web (path-based) is enabled via usePathUrlStrategy()
- Debug banner disabled in MaterialApp
- Analytics/Crashlytics included; consider gating during local development if needed

## Development Workflow

Common scripts:
```
flutter pub get
dart run build_runner build --delete-conflicting-outputs
flutter analyze
flutter test
```

Analyzers and style:
- See analysis_options.yaml for lints
- Prefer immutable models (freezed) and typed JSON with json_serializable
- Keep BLoC layers pure and UI thin

Routing:
- GoRouter is configured in lib/services/navigation/
- If you add routes and use annotations/builders, rerun build_runner

State:
- Observe events with custom bloc observer (lib/bloc/bloc_observer)

## Testing

Run unit/widget tests:
```
flutter test
```

Add tests under test/ mirroring lib/ structure when possible.

## Build and Release

Web (release):
```
flutter build web
```

Android (APK/AAB):
```
flutter build apk
flutter build appbundle
```

iOS (release):
```
flutter build ios
```
Then archive/sign via Xcode for TestFlight/App Store.

## Roadmap and Vision

- XRPL-first: Token issuance, escrow, and DEX primitives underpin core marketplace flows
- Phase progression and planned features: docs/ROADMAP.md
- Strategic overview and hybrid (XRPL + advanced programmability) context: docs/OVERVIEW.md

## Known/Planned Integrations

- Wallets: MetaMask/Keplr via web helpers (web/), with XRPL-centric flows as the target architecture
- Off-chain metadata for product details referenced by on-chain identifiers
- Reputation and governance features aligned with roadmap phases

## Troubleshooting

- Missing generated files: Run build_runner
- Firebase init issues:
  - Web: verify kIsWeb block config and that your Firebase project exists
  - Android/iOS: ensure native config files are present and bundle IDs match
- CocoaPods errors: run `cd ios && pod repo update && pod install`, then retry builds
- Android Gradle errors: open Android Studio, sync Gradle, ensure correct JDK

## Contributing

- Fork and create feature branches
- Follow BLoC and repository patterns used in lib/
- Run analyzers and tests before PRs
- Coordinate on roadmap-aligned tasks to avoid conflicts

## Support

Email: Randy@kaitechcorp.com

## Acknowledgements

- Flutter, Firebase, XRPL community, and open-source ecosystems supporting blockchain-enabled apps
