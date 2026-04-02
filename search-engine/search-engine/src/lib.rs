pub mod trie;
pub mod engine;
pub mod tokenizer;
pub mod morphology;
pub mod morphology_engine;
pub mod odrednica;
pub mod odrednica_engine;
pub mod naslov;
pub mod naslov_engine;
pub mod text_utils;

pub use engine::{SearchEngine, SearchResult, DocumentMetadata};
pub use morphology::{WordType, WordEntry, MorphologyTrieNode};
pub use morphology_engine::MorphologyEngine;
pub use odrednica::OdrednicaEntry;
pub use odrednica_engine::OdrednicaEngine;
pub use naslov::NaslovEntry;
pub use naslov_engine::NaslovEngine;
pub use trie::TrieNode;

#[derive(Debug, thiserror::Error)]
pub enum SearchError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("Serialization error: {0}")]
    Serialization(#[from] bincode::Error),
    
    #[error("Invalid query: {0}")]
    InvalidQuery(String),
    
    #[error("Document not found: {0}")]
    DocumentNotFound(i32),
}

pub type Result<T> = std::result::Result<T, SearchError>;
