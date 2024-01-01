use cosmwasm_std::StdError;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ContractError {
    #[error("{0}")]
    Std(#[from] StdError),

    #[error("Unauthorized")]
    Unauthorized,
    
    #[error("Listing not found")]
    ListingNotFound,

    #[error("Listing cannot be canceled")]
    CannotCancelListing,

    #[error("Invalid token ID")]
    InvalidTokenId,

    #[error("Invalid price")]
    InvalidPrice
}