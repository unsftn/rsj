use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrieNode {
    pub children: HashMap<char, Box<TrieNode>>,
    pub doc_ids: Vec<i32>,
    pub positions: Vec<i32>,
    pub is_end_of_word: bool,
}

impl TrieNode {
    pub fn new() -> Self {
        Self {
            children: HashMap::new(),
            doc_ids: Vec::new(),
            positions: Vec::new(),
            is_end_of_word: false,
        }
    }

    pub fn add_position(&mut self, doc_id: i32, position: i32) {
        self.doc_ids.push(doc_id);
        self.positions.push(position);
    }

    pub fn get_positions(&self) -> Vec<(i32, i32)> {
        self.doc_ids
            .iter()
            .zip(self.positions.iter())
            .map(|(&doc_id, &pos)| (doc_id, pos))
            .collect()
    }

    pub fn insert_word(&mut self, word: &str, doc_id: i32, position: i32) {
        let mut node = self;
        
        for ch in word.chars() {
            node = node
                .children
                .entry(ch)
                .or_insert_with(|| Box::new(TrieNode::new()));
        }
        
        node.is_end_of_word = true;
        node.add_position(doc_id, position);
    }

    pub fn search_word(&self, word: &str) -> Option<Vec<(i32, i32)>> {
        let mut node = self;
        
        for ch in word.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return None,
            }
        }
        
        if node.is_end_of_word {
            Some(node.get_positions())
        } else {
            None
        }
    }

    pub fn collect_all_positions(&self) -> Vec<(i32, i32)> {
        let mut positions = Vec::new();
        
        if self.is_end_of_word {
            positions.extend(self.get_positions());
        }
        
        for child in self.children.values() {
            positions.extend(child.collect_all_positions());
        }
        
        positions
    }

    pub fn collect_words(&self, prefix: String, words: &mut Vec<String>) {
        if self.is_end_of_word {
            words.push(prefix.clone());
        }
        
        for (&ch, child) in &self.children {
            let mut new_prefix = prefix.clone();
            new_prefix.push(ch);
            child.collect_words(new_prefix, words);
        }
    }

    pub fn count_vocabulary(&self) -> usize {
        let mut count = if self.is_end_of_word { 1 } else { 0 };
        
        for child in self.children.values() {
            count += child.count_vocabulary();
        }
        
        count
    }
}

impl Default for TrieNode {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_search() {
        let mut root = TrieNode::new();
        root.insert_word("hello", 1, 0);
        root.insert_word("hello", 1, 5);
        root.insert_word("world", 2, 0);
        
        let positions = root.search_word("hello").unwrap();
        assert_eq!(positions.len(), 2);
        assert_eq!(positions[0], (1, 0));
        assert_eq!(positions[1], (1, 5));
        
        let positions = root.search_word("world").unwrap();
        assert_eq!(positions.len(), 1);
        assert_eq!(positions[0], (2, 0));
        
        assert!(root.search_word("foo").is_none());
    }

    #[test]
    fn test_collect_words() {
        let mut root = TrieNode::new();
        root.insert_word("hello", 1, 0);
        root.insert_word("help", 1, 1);
        root.insert_word("world", 2, 0);
        
        let mut words = Vec::new();
        root.collect_words(String::new(), &mut words);
        words.sort();
        
        assert_eq!(words, vec!["hello", "help", "world"]);
    }
}
