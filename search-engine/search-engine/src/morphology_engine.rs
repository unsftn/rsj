use crate::morphology::{MorphologyTrieNode, WordEntry, WordType};
use crate::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::path::Path;

#[derive(Serialize, Deserialize)]
struct SerializableMorphologyEngine {
    trie: MorphologyTrieNode,
    suffix_trie: MorphologyTrieNode,
    words: HashMap<i32, WordEntry>,
    next_id: i32,
}

pub struct MorphologyEngine {
    trie: MorphologyTrieNode,
    suffix_trie: MorphologyTrieNode,
    words: HashMap<i32, WordEntry>,
    next_id: i32,
}

impl MorphologyEngine {
    pub fn new() -> Self {
        Self {
            trie: MorphologyTrieNode::new(),
            suffix_trie: MorphologyTrieNode::new(),
            words: HashMap::new(),
            next_id: 1,
        }
    }

    /// Add a word with its base form, type, and grammatical forms
    pub fn add_word(&mut self, base_form: String, word_type: WordType, forms: Vec<String>) -> i32 {
        let word_id = self.next_id;
        self.next_id += 1;

        // Insert base form
        self.trie.insert(&base_form, word_id);

        // Insert reversed base form for suffix search
        let reversed: String = base_form.chars().rev().collect();
        self.suffix_trie.insert(&reversed, word_id);

        // Insert all forms
        for form in &forms {
            self.trie.insert(form, word_id);
        }

        let entry = WordEntry::new(word_id, base_form, word_type, forms);
        self.words.insert(word_id, entry);

        word_id
    }

    /// Add a word with original database ID preserved as metadata
    pub fn add_word_with_original_id(
        &mut self,
        original_id: i32,
        base_form: String,
        word_type: WordType,
        forms: Vec<String>,
    ) -> i32 {
        let word_id = self.next_id;
        self.next_id += 1;

        // Insert base form
        self.trie.insert(&base_form, word_id);

        // Insert reversed base form for suffix search
        let reversed: String = base_form.chars().rev().collect();
        self.suffix_trie.insert(&reversed, word_id);

        // Insert all forms
        for form in &forms {
            self.trie.insert(form, word_id);
        }

        let entry = WordEntry::with_original_id(word_id, original_id, base_form, word_type, forms);
        self.words.insert(word_id, entry);

        word_id
    }

    /// Add a word with explicit ID (useful for database import)
    pub fn add_word_with_id(
        &mut self,
        id: i32,
        base_form: String,
        word_type: WordType,
        forms: Vec<String>,
    ) {
        // Insert base form
        self.trie.insert(&base_form, id);

        // Insert reversed base form for suffix search
        let reversed: String = base_form.chars().rev().collect();
        self.suffix_trie.insert(&reversed, id);

        // Insert all forms
        for form in &forms {
            self.trie.insert(form, id);
        }

        let entry = WordEntry::new(id, base_form, word_type, forms);
        self.words.insert(id, entry);

        // Update next_id if necessary
        if id >= self.next_id {
            self.next_id = id + 1;
        }
    }

    /// Search for words by exact form
    pub fn search_by_form(&self, form: &str) -> Vec<WordEntry> {
        let word_ids = self.trie.search_exact(form);
        word_ids
            .iter()
            .filter_map(|id| self.words.get(id).cloned())
            .collect()
    }

    /// Search for words by prefix (for autocomplete)
    pub fn search_by_prefix(&self, prefix: &str) -> Vec<WordEntry> {
        let word_ids = self.trie.search_prefix(prefix);
        word_ids
            .iter()
            .filter_map(|id| self.words.get(id).cloned())
            .collect()
    }

    /// Search for words whose base form ends with the given suffix
    pub fn search_by_suffix(&self, suffix: &str) -> Vec<WordEntry> {
        let reversed: String = suffix.to_lowercase().chars().rev().collect();
        let word_ids = self.suffix_trie.search_prefix(&reversed);
        word_ids
            .iter()
            .filter_map(|id| self.words.get(id).cloned())
            .collect()
    }

    /// Get a word by its ID
    pub fn get_word(&self, id: i32) -> Option<&WordEntry> {
        self.words.get(&id)
    }

    /// Get statistics
    pub fn get_stats(&self) -> HashMap<String, String> {
        let mut stats = HashMap::new();
        
        stats.insert("total_words".to_string(), self.words.len().to_string());
        
        // Count by word type
        let mut type_counts: HashMap<String, usize> = HashMap::new();
        for word in self.words.values() {
            *type_counts.entry(word.word_type.to_string()).or_insert(0) += 1;
        }
        
        for (word_type, count) in type_counts {
            stats.insert(format!("count_{}", word_type), count.to_string());
        }
        
        stats
    }

    /// Save to file
    pub fn save<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);

        let serializable = SerializableMorphologyEngine {
            trie: self.trie.clone(),
            suffix_trie: self.suffix_trie.clone(),
            words: self.words.clone(),
            next_id: self.next_id,
        };

        bincode::serialize_into(writer, &serializable)?;
        Ok(())
    }

    /// Load from file
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);

        let serializable: SerializableMorphologyEngine = bincode::deserialize_from(reader)?;

        Ok(Self {
            trie: serializable.trie,
            suffix_trie: serializable.suffix_trie,
            words: serializable.words,
            next_id: serializable.next_id,
        })
    }
}

impl Default for MorphologyEngine {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_and_search_word() {
        let mut engine = MorphologyEngine::new();
        
        let id = engine.add_word(
            "run".to_string(),
            WordType::Verb,
            vec!["runs".to_string(), "running".to_string(), "ran".to_string()],
        );
        
        // Search by base form
        let results = engine.search_by_form("run");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].id, id);
        
        // Search by inflected form
        let results = engine.search_by_form("running");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].base_form, "run");
    }

    #[test]
    fn test_homonyms() {
        let mut engine = MorphologyEngine::new();
        
        // "left" as verb (past of leave)
        engine.add_word(
            "leave".to_string(),
            WordType::Verb,
            vec!["left".to_string(), "leaving".to_string()],
        );
        
        // "left" as adjective (opposite of right)
        engine.add_word(
            "left".to_string(),
            WordType::Adjective,
            vec!["lefter".to_string(), "leftest".to_string()],
        );
        
        // Search for "left" should return both
        let results = engine.search_by_form("left");
        assert_eq!(results.len(), 2);
        
        let types: Vec<WordType> = results.iter().map(|w| w.word_type.clone()).collect();
        assert!(types.contains(&WordType::Verb));
        assert!(types.contains(&WordType::Adjective));
    }

    #[test]
    fn test_suffix_search() {
        let mut engine = MorphologyEngine::new();

        engine.add_word(
            "читати".to_string(),
            WordType::Glagol,
            vec!["читам".to_string(), "читаш".to_string()],
        );

        engine.add_word(
            "писати".to_string(),
            WordType::Glagol,
            vec!["пишем".to_string(), "пишеш".to_string()],
        );

        engine.add_word(
            "кућа".to_string(),
            WordType::Imenica,
            vec!["куће".to_string(), "кући".to_string()],
        );

        // Both verbs end in "ати"
        let results = engine.search_by_suffix("ати");
        assert_eq!(results.len(), 2);
        let base_forms: Vec<&str> = results.iter().map(|w| w.base_form.as_str()).collect();
        assert!(base_forms.contains(&"читати"));
        assert!(base_forms.contains(&"писати"));

        // Only кућа ends in "ћа"
        let results = engine.search_by_suffix("ћа");
        assert_eq!(results.len(), 1);
        assert_eq!(results[0].base_form, "кућа");

        // No match
        let results = engine.search_by_suffix("xyz");
        assert!(results.is_empty());
    }

    #[test]
    fn test_prefix_search() {
        let mut engine = MorphologyEngine::new();
        
        engine.add_word(
            "run".to_string(),
            WordType::Verb,
            vec!["runs".to_string(), "running".to_string()],
        );
        
        engine.add_word(
            "runner".to_string(),
            WordType::Noun,
            vec!["runners".to_string()],
        );
        
        // Search with prefix "run"
        let results = engine.search_by_prefix("run");
        assert_eq!(results.len(), 2);
        
        // Search with prefix "runn"
        let results = engine.search_by_prefix("runn");
        assert_eq!(results.len(), 2); // Both have forms starting with "runn"
    }
}
