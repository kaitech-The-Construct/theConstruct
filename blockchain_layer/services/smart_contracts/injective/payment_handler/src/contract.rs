use crate::error::ContractError;
use crate::helpers::validate_beneficiary_address;
use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
use crate::state::{Escrow, State, ESCROW_STATE, load_state, load_escrow, save_state, save_escrow};
use cosmwasm_std::{entry_point, Addr, StdResult, Binary, Deps, to_json_binary};
use cosmwasm_std::{
 BankMsg, Coin, CosmosMsg, DepsMut, Env, MessageInfo, Response, SubMsg, Timestamp,
};
use cw2::set_contract_version; // Assume State is defined in state.rs


const CONTRACT_NAME: &str = "crates.io:payment_handler";
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");
const LOCK_TIME: u64 = 300; // 5 minutes in seconds

#[cfg_attr(not(feature = "library"), entry_point)]
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

// Escrow creation and release logic
pub fn execute(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response, ContractError> {
    match msg {
        ExecuteMsg::CreateEscrow {
            id,
            beneficiary,
            end_time,
            funds,
        } => create_escrow(deps, env, info, id, beneficiary, end_time, funds),
        ExecuteMsg::ReleasePayment { id } => release_payment(deps, env, info, id),
    }
}

fn create_escrow(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    id: String,
    beneficiary: Addr,
    end_time: u64,
    funds: Vec<Coin>,
) -> Result<Response, ContractError> {
    // Validation
    if ESCROW_STATE.may_load(deps.storage, &id)?.is_some() {
        // The id is already in use
        return Err(ContractError::EscrowAlreadyExists {});
    }

    let beneficiary_addr = validate_beneficiary_address(deps.api, &beneficiary.to_string())
        .map_err(|_| ContractError::InvalidBeneficiary)?;

    let end_time_timestamp = Timestamp::from_seconds(end_time);

    if end_time_timestamp <= env.block.time.plus_seconds(LOCK_TIME) {
        // Time is 5 min for demo.
        // In production time will be longer to account for order processing time.
        // The end_time is not in the future
        return Err(ContractError::InvalidEndTime {});
    }

    // Lock the funds into the contract's account and create the escrow
    let escrow = Escrow {
        id: id.clone(),
        payer: info.sender,
        beneficiary: beneficiary_addr,
        funds: funds.clone(),
        end_time: end_time_timestamp,
        released: false,
    };

    // Save the escrow
    save_escrow(deps.storage, &id.clone(), &escrow)?;

    let funds_str = funds
        .iter()
        .map(Coin::to_string)
        .collect::<Vec<_>>()
        .join(", ");
    Ok(Response::new()
        .add_attribute("action", "create_escrow")
        .add_attribute("id", id)
        .add_attribute("beneficiary", beneficiary)
        .add_attribute("end_time", end_time.to_string())
        .add_attribute("funds", funds_str))
}

fn release_payment(
    deps: DepsMut,
    env: Env,
    _info: MessageInfo,
    id: String,
) -> Result<Response, ContractError> {
    // Load the escrow
    let mut escrow = load_escrow(deps.storage, &id.clone())?;

    // Validation
    if escrow.released {
        return Err(ContractError::EscrowNotFound {});
    }

    if env.block.time < escrow.end_time {
        return Err(ContractError::ReleaseNotAllowed {});
    }

    // Transfer the funds to the beneficiary if the time limit is up, or back to the owner otherwise
    let recipient = if env.block.time >= escrow.end_time {
        escrow.beneficiary.clone()
    } else {
        escrow.payer.clone()
    };

    escrow.released = true;
    // Update the escrow as released
    save_escrow(deps.storage, &id.clone(), &escrow)?;

    // Release the funds
    let messages: Vec<SubMsg> = escrow
        .funds
        .into_iter()
        .map(|fund| {
            SubMsg::new(CosmosMsg::Bank(BankMsg::Send {
                to_address: recipient.to_string(),
                amount: vec![fund],
            }))
        })
        .collect();

    Ok(Response::new()
        .add_attribute("action", "release_payment")
        .add_attribute("id", id)
        .add_attribute("recipient", recipient)
        .add_submessages(messages))
}

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    // Query logic
    match msg {
        QueryMsg::GetState {} => query_state(deps),
        QueryMsg::GetEscrow { id }=>{
            let escrow = load_escrow(deps.storage, &id)?;
            to_json_binary(&escrow)
        }
    }
}
fn query_state(deps: Deps) -> StdResult<Binary> {
    let state = load_state(deps.storage)?;
    to_json_binary(&state)
}