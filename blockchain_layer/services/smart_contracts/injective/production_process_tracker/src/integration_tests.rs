#[cfg(test)]
mod tests {
    use crate::contract::{execute, instantiate, query};
    use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
    use crate::state::{ManufacturingProcess, OrderStatus, State};
    use crate::ContractError;
    use cosmwasm_std::testing::{
        mock_dependencies, mock_env, mock_info, MockApi, MockQuerier, MockStorage,
    };
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
        // Run initialization test
        let (deps, _env, owner_addr) = setup_contract();
        // Query to assert the owner was set properly
        let query_msg = QueryMsg::GetState {};
        let query_response = query(deps.as_ref(), _env, query_msg).unwrap();
        let state: State = from_json(&query_response).expect("Failed to deserialize Addr");
        assert_eq!(state.owner, owner_addr);
    }

    #[test]
    fn execute_create_process() {
        // Test creating a new process as owner or manufacturer
        let (mut deps, env, owner_addr) = setup_contract();

        // Execute CreateProcess message
        let create_process_msg = ExecuteMsg::CreateProcess {
            order_id: "order123".to_string(),
            customer_addr: Addr::unchecked("customer123"),
            manufacturer_addr: Addr::unchecked("manufacturer123"),
        };
        let res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_process_msg,
        )
        .unwrap();

        // Ensure a response was returned
        assert_eq!(5, res.attributes.len());

        // Query to check the process status
        let query_msg = QueryMsg::GetProcess {
            order_id: "order123".to_string(),
        };
        let query_response = query(deps.as_ref(), env.clone(), query_msg).unwrap();
        let process: ManufacturingProcess = from_json(&query_response).unwrap();

        // Ensure the process was created successfully
        assert_eq!("order123", process.order_id);
        assert_eq!("customer123", process.customer_addr);
        assert_eq!("manufacturer123", process.manufacturer_addr);
        assert_eq!(OrderStatus::Created, process.status);
    }

    #[test]
    fn execute_update_process() {
        let (mut deps, env, owner_addr) = setup_contract();
        // Execute CreateProcess message
        let create_process_msg = ExecuteMsg::CreateProcess {
            order_id: "order123".to_string(),
            customer_addr: Addr::unchecked("customer123"),
            manufacturer_addr: Addr::unchecked("manufacturer123"),
        };
        let _res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_process_msg,
        )
        .unwrap();

        // Update the process status
        let update_process_msg = ExecuteMsg::UpdateProcess {
            order_id: "order123".to_string(),
            status: OrderStatus::InProgress,
        };
        let res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            update_process_msg,
        )
        .unwrap();

        // Ensure a response was returned
        assert_eq!(0, res.messages.len());

        // Query to check the updated process status
        let query_msg = QueryMsg::GetProcess {
            order_id: "order123".to_string(),
        };
        let query_response = query(deps.as_ref(), env.clone(), query_msg).unwrap();
        let process: ManufacturingProcess = from_json(&query_response).unwrap();

        // Ensure the process status was updated successfully
        assert_eq!(OrderStatus::InProgress, process.status);
    }
    #[test]
    fn execute_update_process_unauthorized() {
        // Check if update process can be attempted by unauthorized address
        let (mut deps, env, owner_addr) = setup_contract();
        // Execute CreateProcess message
        let create_process_msg = ExecuteMsg::CreateProcess {
            order_id: "order123".to_string(),
            customer_addr: Addr::unchecked("customer123"),
            manufacturer_addr: Addr::unchecked("manufacturer123"),
        };
        let _res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_process_msg,
        )
        .unwrap();

        // Update the process status
        let update_process_msg = ExecuteMsg::UpdateProcess {
            order_id: "order123".to_string(),
            status: OrderStatus::InProgress,
        };
        let res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&Addr::unchecked("customer123").to_string(), &[]),
            update_process_msg,
        );

        match res {
            Ok(_) => {
                // The operation succeeded, which is not expected
                panic!("Expected an error, but got Ok");
            }
            Err(error) => match error {
                ContractError::Unauthorized => {}
                _ => {
                    // The error is of a different variant, which is not what we expect
                    panic!("Expected Unauthorized error, but got a different error variant");
                }
            },
        }
    }
}
