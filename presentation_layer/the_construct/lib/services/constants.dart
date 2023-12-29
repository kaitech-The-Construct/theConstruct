const String logo = 'assets/images/logo.png';
const String launchScreen = 'assets/images/launch_screen.png';
const String softwareImage = 'assets/images/software.png';
const String landing_1 =
    'https://storage.googleapis.com/app-images-the-construct-401518/landing-1.png';
const String landing_2 =
    'https://storage.googleapis.com/app-images-the-construct-401518/landing-2.png';
const List<String> walletOptions = ['Select Wallet', 'Keplr', 'Metamask'];

const String overview =
    "The Construct is a groundbreaking decentralized robotics exchange (DREX) that revolutionizes how robot manufacturing and software development coalesce.";
const String overview2 =
    "Designed as an innovative marketplace, it empowers robot manufacturers of all sizes to showcase a variety of robot bodies, while also providing software developers with a platform to offer bespoke software solutions specifically designed for these robots.";
const String tagline =
    "Explore and connect robots with advanced software capabilities!";
const String features = "Core Features";
const String featured = 'Featured';

class LandingPageData {
  final String title;
  final String text;

  LandingPageData(this.title, this.text);
}

final List<LandingPageData> landingPageData = [
  LandingPageData(
    "Marketplace",
    "Browse and trade a diverse range of advanced robot bodies and AI-driven software solutions effortlessly. Our user-friendly interface ensures finding the perfect robotic match is just a few clicks away, aligning precision technology with your unique needs.",
  ),
  LandingPageData(
    "Decentralized",
    "Empower your trading experience with The Construct's decentralized platform, where autonomy meets innovation. Trade with confidence and take control of your digital assets on a platform that's as open as it is secure.",
  ),
  LandingPageData(
    "Customizable",
    "Unleash creativity in robotics like never before. The Construct provides an expansive catalog of customizable robot bodies and software tailor-made for a variety of tasks.",
  ),
  LandingPageData(
    "AI-Enhanced",
    "At The Construct, cutting-edge artificial intelligence meets robust blockchain security. Our AI systems diligently oversee compliance, ensuring that all software updates meet the highest standards of safety and reliability.",
  ),
];

const List<String> navBarTitles = [
  "Marketplace",
  "Design Studio",
  "Manufacturing Hub",
  "Community & Governance",
  "Learning Center",
];