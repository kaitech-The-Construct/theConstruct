#[cfg(test)]
mod tests {
    use crate::contract::{execute, instantiate, query};
    use crate::error::ContractError;
    use crate::msg::{ExecuteMsg, InstantiateMsg, QueryMsg};
    use crate::state::{State, ESCROW_STATE};
    use cosmwasm_std::testing::{
        mock_dependencies, mock_env, mock_info, MockApi, MockQuerier, MockStorage,
    };
    use cosmwasm_std::{coins, from_json, Addr, BankMsg, Coin, OwnedDeps, Uint128};
    use lazy_static::lazy_static;

    lazy_static! {
        static ref ESCROW_1: String = "escrow1".to_string();
    }
    lazy_static! {
        static ref ESCROW_2: String = "escrow2".to_string();
    }
    const LOCK_TIME: u64 = 305; // 5 minutes in seconds
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
    fn successful_escrow_creation() {
        let (mut deps, env, owner_addr) = setup_contract();

        // Define the escrow creation message
        let create_escrow_msg = ExecuteMsg::CreateEscrow {
            id: ESCROW_1.to_string(),
            beneficiary: Addr::unchecked("beneficiary"),
            end_time: env.block.time.plus_seconds(LOCK_TIME).seconds(),
            funds: vec![Coin {
                denom: String::from("robo"),
                amount: Uint128::from(100 as u128),
            }],
        };
        println!("End Time: {}",env.block.time.plus_seconds(LOCK_TIME).seconds());
        // Call the create_escrow function with the message
        let res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_escrow_msg,
        )
        .expect("Should be able to create an escrow!");

        // Check for expected result attributes and messages
        assert_eq!(res.attributes.len(), 5); // check for specific attributes

        // Ensure escrow is stored with the provided details
        let escrow = ESCROW_STATE.load(&deps.storage, &ESCROW_1).unwrap();
        assert_eq!(escrow.beneficiary, Addr::unchecked("beneficiary"));
        // assert other escrow fields
    }

    #[test]
    fn successful_escrow_release() {
        let (mut deps, mut env, owner_addr) = setup_contract();

        // Define the escrow creation message
        let create_escrow_msg = ExecuteMsg::CreateEscrow {
            id: ESCROW_1.to_string(),
            beneficiary: Addr::unchecked("beneficiary"),
            end_time: env.block.time.plus_seconds(LOCK_TIME).seconds(),
            funds: vec![Coin {
                denom: String::from("robo"),
                amount: Uint128::from(100 as u128),
            }],
        };

        // Call the create_escrow function with the message
        let _res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_escrow_msg,
        )
        .expect("Should be able to create an escrow!");

        // Simulate block height after escrow end time
        env.block.time = env.block.time.plus_seconds(300 * 2);

        // Define the escrow release message
        let release_escrow_msg = ExecuteMsg::ReleasePayment {
            id: ESCROW_1.to_string(),
        };

        // Call the release_payment function with the message
        let res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            release_escrow_msg,
        )
        .expect("Escrow should be released after maturity!");

        // Check the response for a bank transfer message
        assert!(
            res.messages
                .iter()
                .any(|msg| matches!(msg.msg, cosmwasm_std::CosmosMsg::Bank(BankMsg::Send { .. }))),
            "Expected a bank transfer message in the response"
        );

        // Verify escrow state is updated (released is true)
        let escrow = ESCROW_STATE.load(&deps.storage, &ESCROW_1.clone()).unwrap();
        assert!(escrow.released, "Escrow should be marked as released");
    }

    #[test]
    fn failed_escrow_creation_with_existing_id() {
        let (mut deps, env, owner_addr) = setup_contract();

        // Assume escrow "escrow1" is already created and stored at this point
        let create_escrow_msg = ExecuteMsg::CreateEscrow {
            id: ESCROW_1.to_string(),
            beneficiary: Addr::unchecked("beneficiary"),
            end_time: env.block.time.plus_seconds(LOCK_TIME).seconds(),
            funds: coins(100, "robo"),
        };

        let create_escrow_msg_2 = ExecuteMsg::CreateEscrow {
            id: ESCROW_1.to_string(),
            beneficiary: Addr::unchecked("beneficiary"),
            end_time: env.block.time.plus_seconds(LOCK_TIME).seconds(),
            funds: coins(100, "robo"),
        };

        let _ = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_escrow_msg,
        )
        .expect("Escrow should be created!");

        // Try to create escrow again with the same id, should fail
        let err = execute(
            deps.as_mut(),
            env,
            mock_info(&owner_addr.to_string(), &[]),
            create_escrow_msg_2,
        )
        .expect_err("Escrow creation should have failed with existing id!");

        match err {
            ContractError::EscrowAlreadyExists {} => (), // expected
            _ => panic!("Unexpected error type: {:?}", err), // check for the specific error type
        }
    }

    #[test]
    fn failed_escrow_release_before_maturity() {
        let (mut deps, env, owner_addr) = setup_contract();

        let create_escrow_msg = ExecuteMsg::CreateEscrow {
            id: ESCROW_2.to_string(),
            beneficiary: Addr::unchecked("beneficiary"),
            end_time: env.block.time.plus_seconds(LOCK_TIME).seconds(),
            funds: coins(100, "robo"),
        };

        let _ = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_escrow_msg,
        )
        .expect("Escrow should be created!");
        // Define the escrow release message
        let release_escrow_msg = ExecuteMsg::ReleasePayment {
            id: ESCROW_2.to_string(),
        };

        // Try to release the escrow before the end_time
        let err = execute(
            deps.as_mut(),
            env,
            mock_info(&owner_addr.to_string(), &[]),
            release_escrow_msg,
        )
        .expect_err("Escrow release should have failed before maturity!");

        match err {
            ContractError::ReleaseNotAllowed {} => (), // expected
            _ => panic!("Unexpected error type: {:?}", err), // check for the specific error type
        }
    }

    #[test]
    fn failed_escrow_release_after_already_released() {
        let (mut deps, mut env, owner_addr) = setup_contract();

        // Define the escrow creation message
        let create_escrow_msg = ExecuteMsg::CreateEscrow {
            id: ESCROW_1.to_string(),
            beneficiary: Addr::unchecked("beneficiary"),
            end_time: env.block.time.plus_seconds(LOCK_TIME).seconds(),
            funds: vec![Coin {
                denom: String::from("robo"),
                amount: Uint128::from(100 as u128),
            }],
        };

        // Call the create_escrow function with the message
        let _res = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            create_escrow_msg,
        )
        .expect("Should be able to create an escrow!");
        
        // Simulate block height after escrow end time
        env.block.time = env.block.time.plus_seconds(300 * 2);

        // Release the escrow first time
        let release_escrow_msg = ExecuteMsg::ReleasePayment {
            id: ESCROW_1.to_string(),
        };
        let release_escrow_msg_2 = ExecuteMsg::ReleasePayment {
            id: ESCROW_1.to_string(),
        };
        let _ = execute(
            deps.as_mut(),
            env.clone(),
            mock_info(&owner_addr.to_string(), &[]),
            release_escrow_msg,
        )
        .unwrap();

        // Try to release the same escrow again, should fail
        let err = execute(
            deps.as_mut(),
            env,
            mock_info(&owner_addr.to_string(), &[]),
            release_escrow_msg_2,
        )
        .expect_err("Second escrow release should have failed!");

        match err {
            ContractError::EscrowNotFound {} => (),          // expected
            _ => panic!("Unexpected error type: {:?}", err), // check for the specific error type
        }
    }
}
