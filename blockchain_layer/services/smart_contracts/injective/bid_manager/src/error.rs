use cosmwasm_std::StdError;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ContractError {
    #[error("{0}")]
    Std(#[from] StdError),
    
    #[error("Unauthorized")]
    Unauthorized,

    #[error("Bid not found for the order")]
    BidNotFound,

    #[error("Incorrect amount of funds sent")]
    IncorrectFunds,

    // Add more custom errors as needed.
}