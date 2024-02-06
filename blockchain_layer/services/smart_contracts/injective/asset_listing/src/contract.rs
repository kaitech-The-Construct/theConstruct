use cosmwasm_std::{entry_point, to_json_binary, Binary, Deps, StdResult};
use cosmwasm_std::{Coin, DepsMut, Env, MessageInfo, Response};
use cw2::set_contract_version;

use crate::error::ContractError;
use crate::helpers::validate_price;
use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
use crate::state::{
    load_listing, load_state, remove_listing, save_listing, save_state, Listing, State,
};

const CONTRACT_NAME: &str = "crates.io:listing_contract";
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");

#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    _msg: InstantiateMsg,
) -> Result<Response, ContractError> {
    set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;
    let state = State { owner: info.sender };
    save_state(deps.storage, &state)?;

    Ok(Response::new()
        .add_attribute("method", "instantiate")
        .add_attribute("owner", state.owner))
}

#[entry_point]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response, ContractError> {
    match msg {
        ExecuteMsg::CreateListing {
            listing_id,
            token_id,
            prices,
            quantity
        } => create_listing(deps, info, listing_id, token_id, prices, quantity),
        ExecuteMsg::CancelListing { listing_id } => cancel_listing(deps, info, listing_id),
        ExecuteMsg::UpdateListing {
            listing_id,
            token_id,
            prices,
            quantity
        } => update_listing(deps, info, listing_id, token_id, prices, quantity),
        ExecuteMsg::PurchaseItem {
            listing_id,
            buyer,
            quantity,
        } => purchase_item(deps, info, listing_id, buyer, quantity),
        ExecuteMsg::MakeOffer {
            listing_id,
            buyer,
            price,
            quantity,
        } => make_offer(deps, info, listing_id, buyer, price, quantity),
        ExecuteMsg::AcceptOffer {
            listing_id,
            offer_id,
        } => accept_offer(deps, info, listing_id, offer_id),
        ExecuteMsg::WithdrawOffer {
            listing_id,
            offer_id,
        } => withdraw_offer(deps, info, listing_id, offer_id),
        ExecuteMsg::CompleteTransaction {
            listing_id,
            buyer,
            seller,
        } => complete_transaction(deps, info, listing_id, buyer, seller),
        ExecuteMsg::ReportIssue {
            listing_id,
            buyer,
            seller,
            issue,
        } => report_issue(deps, info, listing_id, buyer, seller, issue),
        ExecuteMsg::ResolveDispute {
            dispute_id,
            resolution,
        } => resolve_dispute(deps, info, dispute_id, resolution),
    }
}

// Implementation of create_listing function
pub fn create_listing(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    token_id: String,
    prices: Vec<Coin>,
    quantity: u64,
) -> Result<Response, ContractError> {
    // Validation: Check if the sender is the contract owner
    let state = load_state(deps.storage)?;
    if info.sender != state.owner {
        return Err(ContractError::Unauthorized {});
    }

    // Check if the token_id is empty and return an error if it is
    if token_id.is_empty() {
        return Err(ContractError::InvalidTokenId {}); // You need to define the InvalidTokenId error in your ContractError enum.
    }
    // Validate price
    let _ = validate_price(prices.clone());

    let listing = Listing {
        listing_id,
        seller: info.sender,
        token_id,
        prices,
        quantity
    };

    // Save the new listing in state
    save_listing(deps.storage, listing_id, &listing)?;

    Ok(Response::new()
        .add_attribute("action", "create_listing")
        .add_attribute("token_id", listing.token_id)
        .add_attribute("listing_id", listing.listing_id.to_string())
        .add_attributes(
            listing
                .prices
                .iter()
                .enumerate()
                .map(|(index, coin)| {
                    (
                        format!("price_{}", index + 1), // Use a unique key for each price
                        coin.to_string(),               // Convert each price to a string
                    )
                })
                .collect::<Vec<_>>(),
        ))
}

// Implementation of cancel_listing function
pub fn cancel_listing(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let listing = load_listing(deps.storage, listing_id)?;

    // Ensure the sender is the owner of the listing
    if listing.seller != info.sender {
        return Err(ContractError::Unauthorized {});
    }

    // Remove the listing from state
    remove_listing(deps.storage, listing_id);

    Ok(Response::new()
        .add_attribute("action", "cancel_listing")
        .add_attribute("listing_id", listing_id.to_string()))
}

// Implementation of update_listing function
pub fn update_listing(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    token_id: String,
    prices: Vec<Coin>,
    quantity: u64,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let mut listing = load_listing(deps.storage, listing_id)?;

    // Ensure the sender is the owner of the listing
    if listing.seller != info.sender {
        return Err(ContractError::Unauthorized {});
    }

    // Update the listing
    listing.token_id = token_id;
    listing.prices = prices;
    listing.quantity = quantity;

    // Save the updated listing in state
    save_listing(deps.storage, listing_id, &listing)?;

    Ok(Response::new()
        .add_attribute("action", "update_listing")
        .add_attribute("token_id", listing.token_id)
        .add_attribute("listing_id", listing.listing_id.to_string())
        .add_attributes(
            listing
                .prices
                .iter()
                .enumerate()
                .map(|(index, coin)| {
                    (
                        format!("price_{}", index + 1), // Use a unique key for each price
                        coin.to_string(),               // Convert each price to a string
                    )
                })
                .collect::<Vec<_>>(),
        ))
}

// Implementation of purchase_item function
pub fn purchase_item(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    buyer: String,
    quantity: u64,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let listing = load_listing(deps.storage, listing_id)?;

    // Ensure the buyer has enough funds to purchase the item
    let mut total_price = 0u128;
    for price in listing.prices.iter() {
        total_price += price.amount.u128();
    }
    if info.funds.amount < total_price {
        return Err(ContractError::InsufficientFunds {});
    }

    // Deduct the funds from the buyer's account
    info.funds.amount -= total_price;

    // Transfer the item to the buyer
    // TODO: Implement the transfer logic

    // Save the transaction details
    // TODO: Implement the save_transaction_details logic

    Ok(Response::new()
        .add_attribute("action", "purchase_item")
        .add_attribute("listing_id", listing_id.to_string())
        .add_attribute("buyer", buyer)
        .add_attribute("quantity", quantity.to_string())
        .add_attribute("total_price", total_price.to_string()))
}

// Implementation of make_offer function
pub fn make_offer(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    buyer: String,
    price: Coin,
    quantity: u64,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let listing = load_listing(deps.storage, listing_id)?;

    // Ensure the buyer has enough funds to make the offer
    if info.funds.amount < price.amount {
        return Err(ContractError::InsufficientFunds {});
    }

    // Deduct the funds from the buyer's account
    info.funds.amount -= price.amount;

    // Save the offer details
    // TODO: Implement the save_offer_details logic

    Ok(Response::new()
        .add_attribute("action", "make_offer")
        .add_attribute("listing_id", listing_id.to_string())
        .add_attribute("buyer", buyer)
        .add_attribute("price", price.to_string())
        .add_attribute("quantity", quantity.to_string()))
}

// Implementation of accept_offer function
pub fn accept_offer(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    offer_id: u64,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let listing = load_listing(deps.storage, listing_id)?;

    // Fetch the offer
    let offer = load_offer(deps.storage, offer_id)?;

    // Ensure the offer is valid
    if offer.listing_id != listing_id {
        return Err(ContractError::InvalidOffer {});
    }
    if offer.buyer != info.sender {
        return Err(ContractError::Unauthorized {});
    }

    // Deduct the funds from the buyer's account
    info.funds.amount -= offer.price.amount;

    // Transfer the item to the buyer
    // TODO: Implement the transfer logic

    // Save the transaction details
    // TODO: Implement the save_transaction_details logic

    Ok(Response::new()
        .add_attribute("action", "accept_offer")
        .add_attribute("listing_id", listing_id.to_string())
        .add_attribute("offer_id", offer_id.to_string())
        .add_attribute("buyer", offer.buyer)
        .add_attribute("price", offer.price.to_string())
        .add_attribute("quantity", offer.quantity.to_string()))
}

// Implementation of withdraw_offer function
pub fn withdraw_offer(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    offer_id: u64,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let listing = load_listing(deps.storage, listing_id)?;

    // Fetch the offer
    let offer = load_offer(deps.storage, offer_id)?;

    // Ensure the offer is valid
    if offer.listing_id != listing_id {
        return Err(ContractError::InvalidOffer {});
    }
    if offer.buyer != info.sender {
        return Err(ContractError::Unauthorized {});
    }

    // Refund the buyer's funds
    info.funds.amount += offer.price.amount;

    // Remove the offer from state
    remove_offer(deps.storage, offer_id);

    Ok(Response::new()
        .add_attribute("action", "withdraw_offer")
        .add_attribute("listing_id", listing_id.to_string())
        .add_attribute("offer_id", offer_id.to_string())
        .add_attribute("buyer", offer.buyer)
        .add_attribute("price", offer.price.to_string())
        .add_attribute("quantity", offer.quantity.to_string()))
}

// Implementation of complete_transaction function
pub fn complete_transaction(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    buyer: String,
    seller: String,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let listing = load_listing(deps.storage, listing_id)?;

    // Ensure the buyer and seller are correct
    if buyer != info.sender {
        return Err(ContractError::Unauthorized {});
    }
    if seller != listing.seller {
        return Err(ContractError::Unauthorized {});
    }

    // Transfer the item to the buyer
    // TODO: Implement the transfer logic

    // Save the transaction details
    // TODO: Implement the save_transaction_details logic

    Ok(Response::new()
        .add_attribute("action", "complete_transaction")
        .add_attribute("listing_id", listing_id.to_string())
        .add_attribute("buyer", buyer)
        .add_attribute("seller", seller))
}

// Implementation of report_issue function
pub fn report_issue(
    deps: DepsMut,
    info: MessageInfo,
    listing_id: u64,
    buyer: String,
    seller: String,
    issue: String,
) -> Result<Response, ContractError> {
    // Fetch the listing
    let listing = load_listing(deps.storage, listing_id)?;

    // Ensure the buyer and seller are correct
    if buyer != info.sender {
        return Err(ContractError::Unauthorized {});
    }
    if seller != listing.seller {
        return Err(ContractError::Unauthorized {});
    }

    // Save the issue report
    // TODO: Implement the save_issue_report logic

    Ok(Response::new()
        .add_attribute("action", "report_issue")
        .add_attribute("listing_id", listing_id.to_string())
        .add_attribute("buyer", buyer)
        .add_attribute("seller", seller)
        .add_attribute("issue", issue))
}

// Implementation of resolve_dispute function
pub fn resolve_dispute(
    deps: DepsMut,
    info: MessageInfo,
    dispute_id: u64,
    resolution: String,
) -> Result<Response, ContractError> {
    // Fetch the dispute
    let dispute = load_dispute(deps.storage, dispute_id)?;

    // Ensure the dispute is valid
    if dispute.listing_id != dispute_id {
        return Err(ContractError::InvalidDispute {});
    }
    if dispute.buyer != info.sender {
        return Err(ContractError::Unauthorized {});
    }

    // Resolve the dispute
    // TODO: Implement the resolve_dispute logic

    Ok(Response::new()
        .add_attribute("action", "resolve_dispute")
        .add_attribute("dispute_id", dispute_id.to_string())
        .add_attribute("resolution", resolution))
}

pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    // Query logic
    match msg {
        QueryMsg::GetListing { listing_id } => {
            let listing = load_listing(deps.storage, listing_id)?;
            to_json_binary(&listing)
        }
        QueryMsg::GetState {} => query_state(deps),
        QueryMsg::GetAllListings {} => { /* Get all listings implementation */ },
        QueryMsg::GetSellerListings {} => { /* Get seller listings implementation */ },
        QueryMsg::GetBuyerOffers {} => { /* Get buyer offers implementation */ },
        QueryMsg::GetListingOffers {} => { /* Get listing offers implementation */ },
        QueryMsg::GetTransactionDetails {} => { /* Get transaction details implementation */ },
        QueryMsg::GetDisputes {} => { /* Get disputes implementation */ },
        QueryMsg::GetResolvedDisputes {} => { /* Get resolved disputes implementation */ },
        QueryMsg::GetPlatformStatistics {} => { /* Get platform statistics implementation */ },
        QueryMsg::GetSellerRatings {} => { /* Get seller ratings implementation */ },
    }
}

fn query_state(deps: Deps) -> StdResult<Binary> {
    let state = load_state(deps.storage)?;
    to_json_binary(&state)
}
