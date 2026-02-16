use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Grammatical word type/part of speech
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum WordType {
    // English word types
    Noun,
    Verb,
    Adjective,
    Adverb,
    Pronoun,
    Preposition,
    Conjunction,
    Interjection,
    Article,
    Numeral,
    Participle,
    // Serbian word types (Srpski)
    Imenica,    // noun
    Glagol,     // verb
    Pridev,     // adjective
    Prilog,     // adverb
    Zamenica,   // pronoun
    Predlog,    // preposition
    Veznik,     // conjunction
    Uzvik,      // interjection
    Recca,      // particle
    Broj,       // numeral
    Other(String),
}

impl WordType {
    pub fn from_str(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            // English
            "noun" | "n" => WordType::Noun,
            "verb" | "v" => WordType::Verb,
            "adjective" | "adj" => WordType::Adjective,
            "adverb" | "adv" => WordType::Adverb,
            "pronoun" | "pron" => WordType::Pronoun,
            "preposition" | "prep" => WordType::Preposition,
            "conjunction" | "conj" => WordType::Conjunction,
            "interjection" | "interj" => WordType::Interjection,
            "article" | "art" => WordType::Article,
            "numeral" | "num" => WordType::Numeral,
            "participle" | "part" => WordType::Participle,
            // Serbian
            "imenica" => WordType::Imenica,
            "glagol" => WordType::Glagol,
            "pridev" => WordType::Pridev,
            "prilog" => WordType::Prilog,
            "zamenica" => WordType::Zamenica,
            "predlog" => WordType::Predlog,
            "veznik" => WordType::Veznik,
            "uzvik" => WordType::Uzvik,
            "recca" | "recce" => WordType::Recca,
            "broj" => WordType::Broj,
            other => WordType::Other(other.to_string()),
        }
    }

    pub fn to_string(&self) -> String {
        match self {
            // English
            WordType::Noun => "noun".to_string(),
            WordType::Verb => "verb".to_string(),
            WordType::Adjective => "adjective".to_string(),
            WordType::Adverb => "adverb".to_string(),
            WordType::Pronoun => "pronoun".to_string(),
            WordType::Preposition => "preposition".to_string(),
            WordType::Conjunction => "conjunction".to_string(),
            WordType::Interjection => "interjection".to_string(),
            WordType::Article => "article".to_string(),
            WordType::Numeral => "numeral".to_string(),
            WordType::Participle => "participle".to_string(),
            // Serbian
            WordType::Imenica => "imenica".to_string(),
            WordType::Glagol => "glagol".to_string(),
            WordType::Pridev => "pridev".to_string(),
            WordType::Prilog => "prilog".to_string(),
            WordType::Zamenica => "zamenica".to_string(),
            WordType::Predlog => "predlog".to_string(),
            WordType::Veznik => "veznik".to_string(),
            WordType::Uzvik => "uzvik".to_string(),
            WordType::Recca => "recca".to_string(),
            WordType::Broj => "broj".to_string(),
            WordType::Other(s) => s.clone(),
        }
    }
}

/// A word entry with its base form, type, and all grammatical forms
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WordEntry {
    pub id: i32,
    pub original_id: Option<i32>,  // Original database ID (if imported)
    pub base_form: String,
    pub word_type: WordType,
    pub forms: Vec<String>,
}

impl WordEntry {
    pub fn new(id: i32, base_form: String, word_type: WordType, forms: Vec<String>) -> Self {
        Self {
            id,
            original_id: None,
            base_form,
            word_type,
            forms,
        }
    }

    pub fn with_original_id(id: i32, original_id: i32, base_form: String, word_type: WordType, forms: Vec<String>) -> Self {
        Self {
            id,
            original_id: Some(original_id),
            base_form,
            word_type,
            forms,
        }
    }
}

/// Trie node for morphological search
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MorphologyTrieNode {
    pub children: HashMap<char, Box<MorphologyTrieNode>>,
    /// IDs of words that have this exact form
    pub word_ids: Vec<i32>,
}

impl MorphologyTrieNode {
    pub fn new() -> Self {
        Self {
            children: HashMap::new(),
            word_ids: Vec::new(),
        }
    }

    pub fn insert(&mut self, form: &str, word_id: i32) {
        let form_lower = form.to_lowercase();
        let mut node = self;

        for ch in form_lower.chars() {
            node = node
                .children
                .entry(ch)
                .or_insert_with(|| Box::new(MorphologyTrieNode::new()));
        }

        if !node.word_ids.contains(&word_id) {
            node.word_ids.push(word_id);
        }
    }

    pub fn search_exact(&self, form: &str) -> Vec<i32> {
        let form_lower = form.to_lowercase();
        let mut node = self;

        for ch in form_lower.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return Vec::new(),
            }
        }

        node.word_ids.clone()
    }

    pub fn search_prefix(&self, prefix: &str) -> Vec<i32> {
        let prefix_lower = prefix.to_lowercase();
        let mut node = self;

        // Navigate to prefix position
        for ch in prefix_lower.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return Vec::new(),
            }
        }

        // Collect all word IDs from this node and descendants
        let mut word_ids = Vec::new();
        self.collect_word_ids(node, &mut word_ids);
        word_ids.sort();
        word_ids.dedup();
        word_ids
    }

    fn collect_word_ids(&self, node: &MorphologyTrieNode, word_ids: &mut Vec<i32>) {
        word_ids.extend(&node.word_ids);

        for child in node.children.values() {
            self.collect_word_ids(child, word_ids);
        }
    }
}

impl Default for MorphologyTrieNode {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_word_type_from_str() {
        assert_eq!(WordType::from_str("noun"), WordType::Noun);
        assert_eq!(WordType::from_str("Verb"), WordType::Verb);
        assert_eq!(WordType::from_str("ADJ"), WordType::Adjective);
    }

    #[test]
    fn test_trie_insert_and_search() {
        let mut trie = MorphologyTrieNode::new();
        
        trie.insert("run", 1);
        trie.insert("runs", 1);
        trie.insert("running", 1);
        trie.insert("ran", 1);
        
        let results = trie.search_exact("running");
        assert_eq!(results, vec![1]);
        
        let no_results = trie.search_exact("walk");
        assert!(no_results.is_empty());
    }

    #[test]
    fn test_trie_prefix_search() {
        let mut trie = MorphologyTrieNode::new();
        
        trie.insert("run", 1);
        trie.insert("runs", 1);
        trie.insert("running", 1);
        trie.insert("runner", 2);
        
        let results = trie.search_prefix("run");
        assert_eq!(results.len(), 2);
        assert!(results.contains(&1));
        assert!(results.contains(&2));
    }

    #[test]
    fn test_multiple_words_same_form() {
        let mut trie = MorphologyTrieNode::new();
        
        // "left" can be verb (past of leave) or adjective (opposite of right)
        trie.insert("left", 1); // leave
        trie.insert("left", 2); // left (adjective)
        
        let results = trie.search_exact("left");
        assert_eq!(results.len(), 2);
        assert!(results.contains(&1));
        assert!(results.contains(&2));
    }
}
