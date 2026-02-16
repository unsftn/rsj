use serde::{Deserialize, Serialize};

/// A dictionary entry (odrednica) with its word, variants, type, and metadata.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OdrednicaEntry {
    pub id: i32,
    pub original_id: i32,
    pub rec: String,
    pub varijante: Vec<String>,
    pub vrsta: i32,
    pub rbr_homonima: Option<i32>,
    pub ociscena_rec: String,
}

impl OdrednicaEntry {
    pub fn new(
        id: i32,
        original_id: i32,
        rec: String,
        varijante: Vec<String>,
        vrsta: i32,
        rbr_homonima: Option<i32>,
        ociscena_rec: String,
    ) -> Self {
        Self {
            id,
            original_id,
            rec,
            varijante,
            vrsta,
            rbr_homonima,
            ociscena_rec,
        }
    }
}
