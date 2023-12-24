use cosmwasm_std::{
    entry_point, to_json_binary, Addr, Binary, Deps, DepsMut, Env, MessageInfo, Response, StdResult,
};
use cw2::set_contract_version;

use crate::error::ContractError;
use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
use crate::state::{
    load_process, load_state, save_process, save_state, ManufacturingProcess, OrderStatus, State,
    PROCESSES,
};

const CONTRACT_NAME: &str = "crates.io:process_tracker";
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
    env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response, ContractError> {
    match msg {
        ExecuteMsg::CreateProcess {
            order_id,
            customer_addr,
            manufacturer_addr,
        } => create_process(deps, order_id, customer_addr, manufacturer_addr),
        ExecuteMsg::UpdateProcess { order_id, status } => {
            update_process(deps, env, info, order_id, status)
        }
    }
}

fn create_process(
    deps: DepsMut,
    order_id: String,
    customer_addr: Addr,
    manufacturer_addr: Addr,
) -> Result<Response, ContractError> {
    //Validation
    if PROCESSES.may_load(deps.storage, &order_id)?.is_some() {
        // The id is already in use
        return Err(ContractError::ProcessAlreadyExists {});
    }

    let process = ManufacturingProcess::new(
        order_id.clone(),
        customer_addr.clone(),
        manufacturer_addr.clone(),
    );
    save_process(deps.storage, &order_id, &process)?;

    Ok(Response::new()
        .add_attribute("action", "create_process")
        .add_attribute("order_id", order_id)
        .add_attribute("customer_addr", customer_addr.as_str())
        .add_attribute("manufacturer_addr", manufacturer_addr.as_str())
        .add_attribute("status", "Created"))
}

pub fn update_process(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    order_id: String,
    status: OrderStatus,
) -> Result<Response, ContractError> {
    let mut process = load_process(deps.storage, &order_id.clone())?;
    let state = load_state(deps.storage)?;

    // Validation: Check if the sender is the authorized owner
    if info.sender != state.owner && info.sender != process.manufacturer_addr {
        return Err(ContractError::Unauthorized {});
    }

    // Update the status
    process.status = status;

    save_process(deps.storage, &order_id, &process)?;

    Ok(Response::new()
        .add_attribute("action", "update_process")
        .add_attribute("order_id", order_id)
        .add_attribute("status", format!("{:?}", process.status)))
}

#[entry_point]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    // Query logic
    match msg {
        QueryMsg::GetState {} => query_state(deps),
        QueryMsg::GetProcess { order_id } => {
            let process = load_process(deps.storage, &order_id)?;
            to_json_binary(&process)
        }
    }
}
fn query_state(deps: Deps) -> StdResult<Binary> {
    let state = load_state(deps.storage)?;
    to_json_binary(&state)
}
