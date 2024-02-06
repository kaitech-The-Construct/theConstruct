#[cfg(test)]
mod tests {
    use crate::contract::{execute, instantiate, query};
    use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
    use crate::state::{State, Listing};
    use cosmwasm_std::testing::{mock_dependencies, mock_env, mock_info, MockApi, MockStorage, MockQuerier};
    use cosmwasm_std::{coins, from_json, Addr, OwnedDeps};

    fn setup_contract() -> (
        OwnedDeps<MockStorage, MockApi, MockQuerier>,
        cosmwasm_std::Env,
        Addr,
    ) {
        let mut deps = mock_dependencies();
        let env = mock_env();
        // Instantiate the contract
        let mock_api = MockApi::default().with_prefix("inj");
        let owner_addr = mock_api.addr_make("creator");
        let msg = InstantiateMsg {
            owner: owner_addr.clone(),
        };
        let _res = instantiate(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &coins(1, "inj")),
            msg,
        )
        .unwrap();
        // Return dependencies, block environment, and owner address
        (deps, env, owner_addr)
    }

    #[test]
    fn proper_initialization() {
        let (deps, _env, owner_addr) = setup_contract();
        // Query to assert the owner was set properly
        let query_msg = QueryMsg::GetState {};
        let query_response = query(deps.as_ref(), _env, query_msg).unwrap();
        let state: State = from_json(&query_response).expect("Failed to deserialize Addr");
        assert_eq!(state.owner, owner_addr);
    }
    #[test]
    fn create_listing_success() {
        let (mut deps, env, owner_addr) = setup_contract();

        // Define the message for creating a listing
        let create_listing_msg = ExecuteMsg::CreateListing {
            listing_id: 1,
            token_id: "token1".to_string(),
            prices: coins(1000, "token"),
            quantity: 10
        };

        // Execute the contract's create_listing function
        let res = execute(deps.as_mut(), env.clone(), mock_info(&owner_addr.to_string(), &[]), create_listing_msg).unwrap();
        assert_eq!(res.attributes.len(), 4); // check for expected attributes count

        // Query the created listing to ensure it reflects the updates made by create_listing
        let query_msg = QueryMsg::GetListing { listing_id: 1 };
        let listing_binary = query(deps.as_ref(), env.clone(), query_msg).unwrap();
        let listing: Listing = from_json(&listing_binary).unwrap();
        assert_eq!(listing.token_id, "token1".to_string());
        assert_eq!(listing.prices, coins(1000, "token"));
    }
    
    #[test]
    fn cancel_listing_success() {
        let (mut deps, env, owner_addr) = setup_contract();

        let create_listing_msg = ExecuteMsg::CreateListing {
            listing_id: 1,
            seller: todo!(),
            price: todo!(),
            metadata: todo!(),
        };

        // Execute the contract's create_listing function
        let _res = execute(deps.as_mut(), env.clone(), mock_info(&owner_addr.to_string(), &[]), create_listing_msg).unwrap();

        // Execute cancel_listing function
        let cancel_listing_msg = ExecuteMsg::CancelListing {
            listing_id: "1",
        };
        let res = execute(deps.as_mut(), env.clone(), mock_info(&owner_addr.to_string(), &[]), cancel_listing_msg).unwrap();
        
        // Check the expected response
        assert_eq!(res.attributes.len(), 2); // check for expected attributes count
    }

}