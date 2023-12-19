use cosmwasm_std::{
    attr, entry_point, to_json_binary, Binary, Deps, DepsMut, Env, MessageInfo, Response, StdResult,
};
use cw2::set_contract_version;

use crate::error::ContractError;
use crate::helpers::generate_order_id;
use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
use crate::state::{load_order, load_state, save_order, save_state, Order, OrderStatus, State};

// Error file needs to be integrated.
// version info for migration info
const CONTRACT_NAME: &str = "crates.io:order_placer";
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");

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

    Ok(Response::new().add_attributes(vec![
        attr("method", "instantiate"),
        attr("owner", state.owner),
    ]))
}

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn execute(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> Result<Response, ContractError> {
    match msg {
        ExecuteMsg::PlaceOrder {
            product_specification,
            quantity,
            deadline,
        } => try_place_order(deps, env, info, product_specification, quantity, deadline),
    }
}

fn try_place_order(
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    product_specification: String,
    quantity: u64,
    deadline: u64,
) -> Result<Response, ContractError> {
    let state = load_state(deps.storage)?;
    if info.sender != state.owner {
        return Err(ContractError::Unauthorized {});
    }

    // Validations
    // validate_deadline(deadline, &env)?;
    // validate_funds_sent(&funds)?;

    let order_id = generate_order_id(&env);
    let new_order = Order {
        id: order_id.clone(),
        creator: info.sender.to_string(),
        product_specification,
        quantity,
        deadline,
        status: OrderStatus::Open,
    };
    save_order(deps.storage, &order_id, &new_order)?;

    Ok(Response::new().add_attributes(vec![
        attr("method", "place_order"),
        attr("order_id", order_id),
        attr("status", "open"),
    ]))
}

#[cfg_attr(not(feature = "library"), entry_point)]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    // Query logic
    match msg {
        QueryMsg::GetOrder { order_id } => {
            let order = load_order(deps.storage, &order_id)?;
            to_json_binary(&order)
        }
        QueryMsg::GetState => query_state(deps),
    }
}

fn query_state(deps: Deps) -> StdResult<Binary> {
    let state = load_state(deps.storage)?;
    to_json_binary(&state)
}
