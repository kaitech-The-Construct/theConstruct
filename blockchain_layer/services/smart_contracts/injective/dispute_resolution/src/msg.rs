use cosmwasm_std::Binary;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, JsonSchema)]
pub struct InstantiateMsg {
    // Define initialization parameters such as eligible resolvers...
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum ExecuteMsg {
    CreateDispute { id: String, claim: String, amount: Uint128 },
    ResolveDispute { id: String, resolution: Resolution },
    // Additional messages for dispute handling...
}

#[derive(Serialize, Deserialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum QueryMsg {
    GetDispute { id: String },
    // Additional queries...
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub enum Resolution {
    InFavorOfClaimant,
    InFavorOfRespondent,
    Split { claimant_share: Uint128 },
}