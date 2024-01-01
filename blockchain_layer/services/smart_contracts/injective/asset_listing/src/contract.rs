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

pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    // Query logic
    match msg {
        QueryMsg::GetListing { listing_id } => {
            let listing = load_listing(deps.storage, listing_id)?;
            to_json_binary(&listing)
        }
        QueryMsg::GetState {} => query_state(deps),
    }
}

fn query_state(deps: Deps) -> StdResult<Binary> {
    let state = load_state(deps.storage)?;
    to_json_binary(&state)
}
