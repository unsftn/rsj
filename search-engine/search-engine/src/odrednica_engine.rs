use crate::morphology::MorphologyTrieNode;
use crate::odrednica::OdrednicaEntry;
use crate::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::path::Path;

#[derive(Serialize, Deserialize)]
struct SerializableOdrednicaEngine {
    trie: MorphologyTrieNode,
    entries: HashMap<i32, OdrednicaEntry>,
    next_id: i32,
}

pub struct OdrednicaEngine {
    trie: MorphologyTrieNode,
    entries: HashMap<i32, OdrednicaEntry>,
    next_id: i32,
}

impl OdrednicaEngine {
    pub fn new() -> Self {
        Self {
            trie: MorphologyTrieNode::new(),
            entries: HashMap::new(),
            next_id: 1,
        }
    }

    /// Add a dictionary entry with all its searchable variants.
    /// Each variant is inserted into the trie for prefix lookup.
    pub fn add_entry(
        &mut self,
        original_id: i32,
        rec: String,
        varijante: Vec<String>,
        vrsta: i32,
        rbr_homonima: Option<i32>,
        ociscena_rec: String,
    ) -> i32 {
        let entry_id = self.next_id;
        self.next_id += 1;

        // Insert all variants into the trie
        for var in &varijante {
            self.trie.insert(var, entry_id);
        }

        let entry = OdrednicaEntry::new(
            entry_id,
            original_id,
            rec,
            varijante,
            vrsta,
            rbr_homonima,
            ociscena_rec,
        );
        self.entries.insert(entry_id, entry);

        entry_id
    }

    /// Search for dictionary entries by prefix across all variants.
    pub fn search_by_prefix(&self, prefix: &str) -> Vec<OdrednicaEntry> {
        let entry_ids = self.trie.search_prefix(prefix);
        entry_ids
            .iter()
            .filter_map(|id| self.entries.get(id).cloned())
            .collect()
    }

    /// Get an entry by its internal ID.
    pub fn get_entry(&self, id: i32) -> Option<&OdrednicaEntry> {
        self.entries.get(&id)
    }

    /// Get statistics about the dictionary index.
    pub fn get_stats(&self) -> HashMap<String, String> {
        let mut stats = HashMap::new();
        stats.insert("total_entries".to_string(), self.entries.len().to_string());

        let mut type_counts: HashMap<i32, usize> = HashMap::new();
        for entry in self.entries.values() {
            *type_counts.entry(entry.vrsta).or_insert(0) += 1;
        }
        for (vrsta, count) in type_counts {
            stats.insert(format!("count_vrsta_{}", vrsta), count.to_string());
        }

        stats
    }

    /// Save to file using bincode serialization.
    pub fn save<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);

        let serializable = SerializableOdrednicaEngine {
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

        let serializable: SerializableOdrednicaEngine = bincode::deserialize_from(reader)?;

        Ok(Self {
            trie: serializable.trie,
            entries: serializable.entries,
            next_id: serializable.next_id,
        })
    }
}

impl Default for OdrednicaEngine {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_and_search_entry() {
        let mut engine = OdrednicaEngine::new();

        let id = engine.add_entry(
            42,
            "абсурд".to_string(),
            vec!["абсурд".to_string(), "absurd".to_string()],
            0,
            None,
            "абсурд".to_string(),
        );

        let results = engine.search_by_prefix("абс");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].id, id);
        assert_eq!(results[0].original_id, 42);
        assert_eq!(results[0].rec, "абсурд");

        // Search by Latin prefix
        let results = engine.search_by_prefix("abs");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].rec, "абсурд");
    }

    #[test]
    fn test_homonyms() {
        let mut engine = OdrednicaEngine::new();

        engine.add_entry(
            1,
            "коса".to_string(),
            vec!["коса".to_string(), "kosa".to_string()],
            0,
            Some(1),
            "коса".to_string(),
        );

        engine.add_entry(
            2,
            "коса".to_string(),
            vec!["коса".to_string(), "kosa".to_string()],
            0,
            Some(2),
            "коса".to_string(),
        );

        let results = engine.search_by_prefix("кос");
        assert_eq!(results.len(), 2);
    }

    #[test]
    fn test_search_by_variant() {
        let mut engine = OdrednicaEngine::new();

        engine.add_entry(
            10,
            "млеко".to_string(),
            vec![
                "млеко".to_string(),
                "млијеко".to_string(),
                "mleko".to_string(),
                "mlijeko".to_string(),
            ],
            0,
            None,
            "млеко".to_string(),
        );

        // Search by ijekavski variant
        let results = engine.search_by_prefix("млије");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].rec, "млеко");

        // Search by Latin variant
        let results = engine.search_by_prefix("mli");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].rec, "млеко");
    }

    #[test]
    fn test_get_entry() {
        let mut engine = OdrednicaEngine::new();

        let id = engine.add_entry(
            5,
            "реч".to_string(),
            vec!["реч".to_string()],
            0,
            None,
            "реч".to_string(),
        );

        let entry = engine.get_entry(id);
        assert!(entry.is_some());
        assert_eq!(entry.unwrap().rec, "реч");

        assert!(engine.get_entry(999).is_none());
    }

    #[test]
    fn test_stats() {
        let mut engine = OdrednicaEngine::new();

        engine.add_entry(1, "реч".to_string(), vec!["реч".to_string()], 0, None, "реч".to_string());
        engine.add_entry(2, "ићи".to_string(), vec!["ићи".to_string()], 1, None, "ићи".to_string());
        engine.add_entry(3, "леп".to_string(), vec!["леп".to_string()], 2, None, "леп".to_string());

        let stats = engine.get_stats();
        assert_eq!(stats.get("total_entries").unwrap(), "3");
        assert_eq!(stats.get("count_vrsta_0").unwrap(), "1");
        assert_eq!(stats.get("count_vrsta_1").unwrap(), "1");
        assert_eq!(stats.get("count_vrsta_2").unwrap(), "1");
    }

    #[test]
    fn test_empty_prefix_search() {
        let engine = OdrednicaEngine::new();
        let results = engine.search_by_prefix("xyz");
        assert!(results.is_empty());
    }
}
