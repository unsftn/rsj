use crate::morphology::MorphologyTrieNode;
use crate::naslov::NaslovEntry;
use crate::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::path::Path;

#[derive(Serialize, Deserialize)]
struct SerializableNaslovEngine {
    trie: MorphologyTrieNode,
    entries: HashMap<i32, NaslovEntry>,
    next_id: i32,
}

pub struct NaslovEngine {
    trie: MorphologyTrieNode,
    entries: HashMap<i32, NaslovEntry>,
    next_id: i32,
}

impl NaslovEngine {
    pub fn new() -> Self {
        Self {
            trie: MorphologyTrieNode::new(),
            entries: HashMap::new(),
            next_id: 1,
        }
    }

    /// Add a publication title/description entry.
    /// Each word in the opis and skracenica is inserted into the trie for prefix lookup.
    pub fn add_entry(
        &mut self,
        original_id: i32,
        skracenica: String,
        opis: String,
        potkorpus: String,
    ) -> i32 {
        let entry_id = self.next_id;
        self.next_id += 1;

        // Tokenize opis and skracenica, insert each word into the trie
        let searchable_text = format!("{} {}", opis, skracenica);
        for word in searchable_text.split_whitespace() {
            let cleaned: String = word.chars()
                .filter(|c| c.is_alphanumeric() || *c == '-')
                .collect();
            if !cleaned.is_empty() {
                self.trie.insert(&cleaned, entry_id);
            }
        }

        let entry = NaslovEntry::new(entry_id, original_id, skracenica, opis, potkorpus);
        self.entries.insert(entry_id, entry);

        entry_id
    }

    /// Search for publication entries by prefix across opis and skracenica words.
    pub fn search_by_prefix(&self, prefix: &str) -> Vec<NaslovEntry> {
        let entry_ids = self.trie.search_prefix(prefix);
        entry_ids
            .iter()
            .filter_map(|id| self.entries.get(id).cloned())
            .collect()
    }

    /// Get an entry by its internal ID.
    pub fn get_entry(&self, id: i32) -> Option<&NaslovEntry> {
        self.entries.get(&id)
    }

    /// Get an entry by its original (database) ID.
    pub fn get_entry_by_original_id(&self, original_id: i32) -> Option<&NaslovEntry> {
        self.entries.values().find(|e| e.original_id == original_id)
    }

    /// Get statistics about the naslov index.
    pub fn get_stats(&self) -> HashMap<String, String> {
        let mut stats = HashMap::new();
        stats.insert("total_entries".to_string(), self.entries.len().to_string());
        stats
    }

    /// Save to file using bincode serialization.
    pub fn save<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);

        let serializable = SerializableNaslovEngine {
            trie: self.trie.clone(),
            entries: self.entries.clone(),
            next_id: self.next_id,
        };

        bincode::serialize_into(writer, &serializable)?;
        Ok(())
    }

    /// Load from file using bincode deserialization.
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);

        let serializable: SerializableNaslovEngine = bincode::deserialize_from(reader)?;

        Ok(Self {
            trie: serializable.trie,
            entries: serializable.entries,
            next_id: serializable.next_id,
        })
    }
}

impl Default for NaslovEngine {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_and_search() {
        let mut engine = NaslovEngine::new();

        engine.add_entry(
            42,
            "Андрић".to_string(),
            "Андрић, Иво: На Дрини ћуприја".to_string(),
            "књижевност".to_string(),
        );

        let results = engine.search_by_prefix("андрић");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].original_id, 42);

        // Search by word in opis
        let results = engine.search_by_prefix("дрин");
        assert_eq!(results.len(), 1);

        // Search by skracenica
        let results = engine.search_by_prefix("андрић");
        assert_eq!(results.len(), 1);
    }

    #[test]
    fn test_no_results() {
        let engine = NaslovEngine::new();
        let results = engine.search_by_prefix("xyz");
        assert!(results.is_empty());
    }

    #[test]
    fn test_multiple_entries() {
        let mut engine = NaslovEngine::new();

        engine.add_entry(
            1,
            "Андрић".to_string(),
            "Андрић, Иво: На Дрини ћуприја".to_string(),
            "књижевност".to_string(),
        );

        engine.add_entry(
            2,
            "Андрић2".to_string(),
            "Андрић, Иво: Травничка хроника".to_string(),
            "књижевност".to_string(),
        );

        // Both should match prefix "андрић"
        let results = engine.search_by_prefix("андрић");
        assert_eq!(results.len(), 2);

        // Only one matches "травнич"
        let results = engine.search_by_prefix("травнич");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].original_id, 2);
    }

    #[test]
    fn test_get_entry_by_original_id() {
        let mut engine = NaslovEngine::new();

        engine.add_entry(
            10,
            "Скр".to_string(),
            "Опис публикације".to_string(),
            "потк".to_string(),
        );

        let entry = engine.get_entry_by_original_id(10);
        assert!(entry.is_some());
        assert_eq!(entry.unwrap().skracenica, "Скр");

        assert!(engine.get_entry_by_original_id(999).is_none());
    }

    #[test]
    fn test_stats() {
        let mut engine = NaslovEngine::new();

        engine.add_entry(1, "A".to_string(), "Opis 1".to_string(), "P1".to_string());
        engine.add_entry(2, "B".to_string(), "Opis 2".to_string(), "P2".to_string());

        let stats = engine.get_stats();
        assert_eq!(stats.get("total_entries").unwrap(), "2");
    }
}
