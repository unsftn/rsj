use serde::{Deserialize, Serialize};

/// A publication title/description entry for prefix search.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NaslovEntry {
    pub id: i32,
    pub original_id: i32,
    pub skracenica: String,
    pub opis: String,
    pub potkorpus: String,
}

impl NaslovEntry {
    pub fn new(
        id: i32,
        original_id: i32,
        skracenica: String,
        opis: String,
        potkorpus: String,
    ) -> Self {
        Self {
            id,
            original_id,
            skracenica,
            opis,
            potkorpus,
        }
    }
}
