// msg.rs
use cosmwasm_std::{ Addr, Coin };
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, JsonSchema)]
pub struct InstantiateMsg {
    pub owner: Addr,
}

// Add other execute messages discussed previously
#[derive(Serialize, Deserialize, JsonSchema)]
pub enum ExecuteMsg {
    CreateListing {
        listing_id: String,
        seller: Addr,
        price: Coin,
        metadata: String,
    },
    CancelListing {
        listing_id: String,
    },
    UpdateListing {
        listing_id: String,
        new_price: Coin,
        new_metadata: String,
    },
    PurchaseItem {
        listing_id: String,
        buyer: Addr,
    },
    MakeOffer {
        listing_id: String,
        buyer: Addr,
        offer: Coin,
    },
    AcceptOffer {
        listing_id: String,
        offer_id: String,
    },
    WithdrawOffer {
        offer_id: String,
    },
    CompleteTransaction {
        transaction_id: String,
    },
    ReportIssue {
        transaction_id: String,
        issue_description: String,
    },
    ResolveDispute {
        dispute_id: String,
    },
    // More execute messages can be added as new features are implemented
}

#[derive(Serialize, Deserialize, JsonSchema)]
pub enum QueryMsg {
    GetListing {
        listing_id: String,
    },
    GetAllListings {},
    GetSellerListings {
        seller: Addr,
    },
    GetBuyerOffers { 
        buyer: Addr,
    },
    GetListingOffers {
        listing_id: String,
    },
    GetTransactionDetails {
        transaction_id: String,
    },
    GetDisputes {},
    GetResolvedDisputes {},
    GetPlatformStatistics {},
    GetSellerRatings {
        seller: Addr,
    },
}