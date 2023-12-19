#[cfg(test)]
mod tests {
    use crate::contract::{execute, instantiate, query};
    use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
    use crate::state::State;
    use cosmwasm_std::testing::{mock_dependencies, mock_env, mock_info, MockApi};
    use cosmwasm_std::{coins, from_json, Addr};

    #[test]
    fn proper_initialization() {
        let mut deps = mock_dependencies();
        let owner_str = "owner";
        let mock_api = MockApi::default().with_prefix("inj");
        let owner_addr = mock_api.addr_make("creator"); // Convert &str to Addr

        let msg = InstantiateMsg {
            owner: owner_addr.to_string(),
        };
        let info = mock_info(&owner_addr.to_string(), &coins(2, "inj")); // Use the same string literal for the owner address
        let env = mock_env();

        // Calling the contract instantiation
        let res = instantiate(deps.as_mut(), env, info, msg).unwrap();
        assert_eq!(0, res.messages.len());

        // Querying the contract state
        let query_msg = QueryMsg::GetState {};
        let binary_result = query(deps.as_ref(), mock_env(), query_msg).unwrap();
        println!("Query Response = {:?}", binary_result);
        let state: State = from_json(&binary_result).unwrap();

        // Here we check if the instantiated state's owner is the same address that was used during instantiation
        assert_eq!(state.owner, owner_addr); // Comparing Addr with Addr
    }

    #[test]
    fn order_placement() {
        let mut deps = mock_dependencies();
        let owner_str = "owner";
        let mock_api = MockApi::default().with_prefix("inj");
        let owner_addr = mock_api.addr_make("creator"); // Convert &str to Addr

        let msg = InstantiateMsg {
            owner: owner_addr.to_string(),
        };
        let info = mock_info(owner_str, &coins(2, "inj"));

        let env = mock_env();
        let _res = instantiate(deps.as_mut(), env.clone(), info.clone(), msg).unwrap();

        // Set up message to place an order
        let order_msg = ExecuteMsg::PlaceOrder {
            product_specification: "Widget".to_string(),
            quantity: 10,
            deadline: env.block.time.plus_seconds(1000).seconds(),
        };

        let res = execute(deps.as_mut(), env.clone(), info.clone(), order_msg).unwrap();
        assert_eq!(res.attributes[2].value, "open");

        // You could then query to confirm that the order was placed successfully by checking if
        // its attributes match the ones we definied above.
    }
}
