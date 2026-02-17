use crate::trie::TrieNode;
use crate::tokenizer::Tokenizer;
use crate::{Result, SearchError};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::path::Path;

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct DocumentMetadata {
    pub title: Option<String>,
    pub author: Option<String>,
}

impl DocumentMetadata {
    pub fn new() -> Self {
        Self::default()
    }
}

#[derive(Debug, Clone)]
pub struct SearchResult {
    pub doc_id: i32,
    pub metadata: DocumentMetadata,
    pub fragments: Vec<String>,
}

#[derive(Serialize, Deserialize)]
struct SerializableEngine {
    forward_trie: TrieNode,
    reverse_trie: TrieNode,
    documents: HashMap<i32, String>,
    doc_metadata: HashMap<i32, DocumentMetadata>,
    token_offsets: HashMap<i32, Vec<(u32, u16)>>,
}

pub struct SearchEngine {
    forward_trie: TrieNode,
    reverse_trie: TrieNode,
    documents: HashMap<i32, String>,
    doc_metadata: HashMap<i32, DocumentMetadata>,
    token_offsets: HashMap<i32, Vec<(u32, u16)>>,
    tokenizer: Tokenizer,
}

impl SearchEngine {
    pub fn new() -> Self {
        Self {
            forward_trie: TrieNode::new(),
            reverse_trie: TrieNode::new(),
            documents: HashMap::new(),
            doc_metadata: HashMap::new(),
            token_offsets: HashMap::new(),
            tokenizer: Tokenizer::new(),
        }
    }

    pub fn add_document(&mut self, doc_id: i32, text: String, metadata: DocumentMetadata) {
        let tokens = self.tokenizer.tokenize(&text);

        for (position, token) in tokens.iter().enumerate() {
            // Insert into forward trie (for prefix/exact search)
            self.forward_trie.insert_word(token, doc_id, position as i32);

            // Insert into reverse trie (for suffix search)
            let reversed: String = token.chars().rev().collect();
            self.reverse_trie.insert_word(&reversed, doc_id, position as i32);
        }

        self.token_offsets.insert(doc_id, self.tokenizer.tokenize_offsets(&text));
        self.documents.insert(doc_id, text);
        self.doc_metadata.insert(doc_id, metadata);
    }

    pub fn search_word(&self, word: &str) -> Vec<(i32, i32)> {
        let word_lower = word.to_lowercase();
        
        // Check if it's a suffix search
        if word_lower.starts_with('~') {
            return self.suffix_search(&word_lower[1..]);
        }
        
        self.forward_trie
            .search_word(&word_lower)
            .unwrap_or_default()
    }

    fn suffix_search(&self, suffix: &str) -> Vec<(i32, i32)> {
        let reversed: String = suffix.chars().rev().collect();
        
        // Navigate to suffix position in reverse trie
        let mut node = &self.reverse_trie;
        for ch in reversed.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return Vec::new(),
            }
        }
        
        // Collect all positions from this node and descendants
        node.collect_all_positions()
    }

    pub fn suffix_word_search(&self, suffix: &str) -> Vec<String> {
        let suffix_lower = suffix.to_lowercase();
        let reversed: String = suffix_lower.chars().rev().collect();
        
        let mut node = &self.reverse_trie;
        for ch in reversed.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return Vec::new(),
            }
        }
        
        let mut words = Vec::new();
        node.collect_words(reversed.clone(), &mut words);
        
        // Reverse the words back to normal
        words.iter().map(|w| w.chars().rev().collect()).collect()
    }

    pub fn prefix_search(&self, prefix: &str) -> Vec<String> {
        let prefix_lower = prefix.to_lowercase();
        
        let mut node = &self.forward_trie;
        for ch in prefix_lower.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return Vec::new(),
            }
        }
        
        let mut words = Vec::new();
        node.collect_words(prefix_lower.clone(), &mut words);
        words
    }

    pub fn search_phrase(
        &self,
        phrase: &str,
        fragment_size: usize,
        mode: &str,
    ) -> Result<Vec<SearchResult>> {
        let tokens = self.tokenizer.tokenize(phrase);
        
        if tokens.is_empty() {
            return Ok(Vec::new());
        }
        
        // Check if any token uses suffix search
        if tokens.iter().any(|t| t.starts_with('~')) {
            return Err(SearchError::InvalidQuery(
                "Suffix search (~) is not supported for phrases".to_string(),
            ));
        }
        
        // Get positions for each word
        let mut word_positions: Vec<Vec<(i32, i32)>> = Vec::new();
        let mut docs_per_word: Vec<HashSet<i32>> = Vec::new();
        
        for token in &tokens {
            let positions = self.search_word(token);
            if positions.is_empty() {
                return Ok(Vec::new());
            }
            
            let docs: HashSet<i32> = positions.iter().map(|(doc_id, _)| *doc_id).collect();
            docs_per_word.push(docs);
            word_positions.push(positions);
        }
        
        // Find documents containing ALL words
        let mut candidate_docs = docs_per_word[0].clone();
        for docs in &docs_per_word[1..] {
            candidate_docs = candidate_docs.intersection(docs).copied().collect();
        }
        
        if candidate_docs.is_empty() {
            return Ok(Vec::new());
        }
        
        // Group first word positions by document
        let mut docs_to_first_positions: HashMap<i32, Vec<i32>> = HashMap::new();
        for &(doc_id, pos) in &word_positions[0] {
            if candidate_docs.contains(&doc_id) {
                docs_to_first_positions.entry(doc_id).or_default().push(pos);
            }
        }
        
        // Find matching phrase positions
        let mut results = Vec::new();
        
        for (doc_id, first_positions) in docs_to_first_positions {
            let matching_positions =
                self.find_phrase_matches(doc_id, &first_positions, &word_positions, tokens.len());
            
            if !matching_positions.is_empty() {
                let metadata = self.doc_metadata.get(&doc_id).cloned().unwrap_or_else(DocumentMetadata::new);
                
                let fragments = match mode {
                    "sentence" => self.generate_sentence_fragments(doc_id, &matching_positions, tokens.len()),
                    _ => self.generate_word_fragments(doc_id, &matching_positions, tokens.len(), fragment_size),
                };
                
                results.push(SearchResult {
                    doc_id,
                    metadata,
                    fragments,
                });
            }
        }
        
        Ok(results)
    }

    fn find_phrase_matches(
        &self,
        doc_id: i32,
        first_positions: &[i32],
        word_positions: &[Vec<(i32, i32)>],
        phrase_length: usize,
    ) -> Vec<i32> {
        if phrase_length == 1 {
            return first_positions.to_vec();
        }
        
        let mut matching_positions = Vec::new();
        
        for &start_pos in first_positions {
            let mut is_match = true;
            
            for i in 1..phrase_length {
                let expected_pos = start_pos + i as i32;
                let found = word_positions[i].iter().any(|&(d, p)| d == doc_id && p == expected_pos);
                
                if !found {
                    is_match = false;
                    break;
                }
            }
            
            if is_match {
                matching_positions.push(start_pos);
            }
        }
        
        matching_positions
    }

    fn generate_word_fragments(
        &self,
        doc_id: i32,
        match_positions: &[i32],
        phrase_length: usize,
        fragment_size: usize,
    ) -> Vec<String> {
        let text = match self.documents.get(&doc_id) {
            Some(t) => t,
            None => return Vec::new(),
        };

        // Use pre-computed offsets if available, else compute on the fly
        let computed;
        let offsets: &[(u32, u16)] = match self.token_offsets.get(&doc_id) {
            Some(cached) => cached,
            None => {
                computed = self.tokenizer.tokenize_offsets(text);
                &computed
            }
        };
        let num_tokens = offsets.len();

        let mut ranges: Vec<(usize, usize, Vec<(usize, usize)>)> = Vec::new();

        for &match_pos in match_positions {
            let match_pos = match_pos as usize;
            let context_before = (fragment_size.saturating_sub(phrase_length)) / 2;
            let context_after = fragment_size.saturating_sub(phrase_length).saturating_sub(context_before);

            let start_pos = match_pos.saturating_sub(context_before);
            let end_pos = (match_pos + phrase_length + context_after).min(num_tokens);

            let match_start_char = offsets.get(match_pos).map_or(0, |o| o.0 as usize);
            let match_end_token = match_pos + phrase_length - 1;
            let mut match_end_char = offsets.get(match_end_token).map_or(text.len(), |o| o.0 as usize);

            if match_end_token < num_tokens {
                match_end_char += offsets[match_end_token].1 as usize;
            }

            ranges.push((start_pos, end_pos, vec![(match_start_char, match_end_char)]));
        }

        let merged_ranges = self.merge_overlapping_ranges(ranges);

        let mut fragments = Vec::new();

        for (start_pos, end_pos, match_char_spans) in merged_ranges {
            let start_char = offsets.get(start_pos).map_or(0, |o| o.0 as usize);
            let mut end_char = offsets.get(end_pos.saturating_sub(1)).map_or(text.len(), |o| o.0 as usize);

            if end_pos > 0 && end_pos - 1 < num_tokens {
                end_char += offsets[end_pos - 1].1 as usize;
            }

            let mut fragment_text = text[start_char..end_char.min(text.len())].trim().to_string();

            // Insert highlight markers
            let mut relative_matches: Vec<(usize, usize)> = match_char_spans
                .iter()
                .map(|&(s, e)| (s.saturating_sub(start_char), e.saturating_sub(start_char)))
                .collect();
            relative_matches.sort_by_key(|&(s, _)| s);

            let mut offset = 0;
            for (match_start, match_end) in relative_matches {
                let adj_start = match_start + offset;
                let adj_end = match_end + offset;

                fragment_text.insert_str(adj_start, "***");
                fragment_text.insert_str(adj_end + 3, "***");
                offset += 6;
            }

            // Add ellipsis
            if start_char > 0 {
                fragment_text = format!("... {}", fragment_text);
            }
            if end_char < text.len() {
                fragment_text = format!("{} ...", fragment_text);
            }

            fragments.push(fragment_text);
        }

        fragments
    }

    fn generate_sentence_fragments(
        &self,
        doc_id: i32,
        match_positions: &[i32],
        phrase_length: usize,
    ) -> Vec<String> {
        let text = match self.documents.get(&doc_id) {
            Some(t) => t,
            None => return Vec::new(),
        };

        // Use pre-computed offsets if available, else compute on the fly
        let computed;
        let offsets: &[(u32, u16)] = match self.token_offsets.get(&doc_id) {
            Some(cached) => cached,
            None => {
                computed = self.tokenizer.tokenize_offsets(text);
                &computed
            }
        };
        let num_tokens = offsets.len();

        let sentences = self.get_sentences(text);

        let mut sentence_ranges: Vec<(usize, usize, Vec<(usize, usize)>)> = Vec::new();

        for &match_pos in match_positions {
            let match_pos = match_pos as usize;
            let match_start_char = offsets.get(match_pos).map_or(0, |o| o.0 as usize);
            let match_end_token = match_pos + phrase_length - 1;
            let mut match_end_char = offsets.get(match_end_token).map_or(text.len(), |o| o.0 as usize);

            if match_end_token < num_tokens {
                match_end_char += offsets[match_end_token].1 as usize;
            }

            // Find containing sentence
            for (sent_idx, &(sent_start, sent_end)) in sentences.iter().enumerate() {
                if sent_start <= match_start_char && match_start_char < sent_end {
                    sentence_ranges.push((sent_idx, sent_idx + 1, vec![(match_start_char, match_end_char)]));
                    break;
                }
            }
        }
        
        if sentence_ranges.is_empty() {
            return Vec::new();
        }
        
        let merged_ranges = self.merge_overlapping_ranges(sentence_ranges);
        
        let mut fragments = Vec::new();
        
        for (start_sent_idx, end_sent_idx, match_char_spans) in merged_ranges {
            let sent_start_char = sentences[start_sent_idx].0;
            let sent_end_char = sentences[end_sent_idx - 1].1;
            
            let mut fragment_text = text[sent_start_char..sent_end_char].trim().to_string();
            
            let mut relative_matches: Vec<(usize, usize)> = match_char_spans
                .iter()
                .map(|&(s, e)| (s.saturating_sub(sent_start_char), e.saturating_sub(sent_start_char)))
                .collect();
            relative_matches.sort_by_key(|&(s, _)| s);
            
            let mut offset = 0;
            for (match_start, match_end) in relative_matches {
                let adj_start = match_start + offset;
                let adj_end = match_end + offset;
                
                fragment_text.insert_str(adj_start, "***");
                fragment_text.insert_str(adj_end + 3, "***");
                offset += 6;
            }
            
            fragments.push(fragment_text);
        }
        
        fragments
    }

    fn get_sentences(&self, text: &str) -> Vec<(usize, usize)> {
        let sentence_regex = regex::Regex::new(r"[.!?]+\s+").unwrap();
        let mut sentences = Vec::new();
        let mut start = 0;
        
        for m in sentence_regex.find_iter(text) {
            sentences.push((start, m.end()));
            start = m.end();
        }
        
        if start < text.len() {
            sentences.push((start, text.len()));
        }
        
        sentences
    }

    fn merge_overlapping_ranges<T: Clone>(
        &self,
        mut ranges: Vec<(usize, usize, Vec<T>)>,
    ) -> Vec<(usize, usize, Vec<T>)> {
        if ranges.is_empty() {
            return Vec::new();
        }
        
        ranges.sort_by_key(|(start, _, _)| *start);
        
        let mut merged = Vec::new();
        let (mut current_start, mut current_end, mut current_matches) = ranges[0].clone();
        
        for (start, end, matches) in ranges.into_iter().skip(1) {
            if start <= current_end {
                current_end = current_end.max(end);
                current_matches.extend(matches);
            } else {
                merged.push((current_start, current_end, current_matches.clone()));
                current_start = start;
                current_end = end;
                current_matches = matches;
            }
        }
        
        merged.push((current_start, current_end, current_matches));
        merged
    }

    pub fn search_words(
        &self,
        words: &[String],
        fragment_size: usize,
        mode: &str,
    ) -> Result<Vec<SearchResult>> {
        if words.is_empty() {
            return Ok(Vec::new());
        }

        // Collect all (doc_id, position) pairs for all words at once
        let mut doc_positions: HashMap<i32, Vec<i32>> = HashMap::new();

        for word in words {
            let positions = self.search_word(word);
            for (doc_id, pos) in positions {
                doc_positions.entry(doc_id).or_default().push(pos);
            }
        }

        // Generate fragments once per document (single tokenization pass)
        let mut results = Vec::new();

        for (doc_id, mut positions) in doc_positions {
            positions.sort();
            positions.dedup();

            let metadata = self
                .doc_metadata
                .get(&doc_id)
                .cloned()
                .unwrap_or_default();

            let fragments = match mode {
                "sentence" => self.generate_sentence_fragments(doc_id, &positions, 1),
                _ => self.generate_word_fragments(doc_id, &positions, 1, fragment_size),
            };

            if !fragments.is_empty() {
                results.push(SearchResult {
                    doc_id,
                    metadata,
                    fragments,
                });
            }
        }

        Ok(results)
    }

    pub fn get_document(&self, doc_id: i32) -> Option<&String> {
        self.documents.get(&doc_id)
    }

    pub fn get_stats(&self) -> HashMap<String, String> {
        let mut stats = HashMap::new();
        
        stats.insert("num_documents".to_string(), self.documents.len().to_string());
        
        let total_chars: usize = self.documents.values().map(|d| d.len()).sum();
        stats.insert("total_chars".to_string(), total_chars.to_string());
        
        let vocab_size = self.forward_trie.count_vocabulary();
        stats.insert("vocabulary_size".to_string(), vocab_size.to_string());
        
        let suffix_enabled = self.reverse_trie.count_vocabulary() > 0;
        stats.insert("suffix_search_enabled".to_string(), suffix_enabled.to_string());
        
        stats
    }

    pub fn save<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        
        let serializable = SerializableEngine {
            forward_trie: self.forward_trie.clone(),
            reverse_trie: self.reverse_trie.clone(),
            documents: self.documents.clone(),
            doc_metadata: self.doc_metadata.clone(),
            token_offsets: self.token_offsets.clone(),
        };
        
        bincode::serialize_into(writer, &serializable)?;
        Ok(())
    }

    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        
        let serializable: SerializableEngine = bincode::deserialize_from(reader)?;
        
        Ok(Self {
            forward_trie: serializable.forward_trie,
            reverse_trie: serializable.reverse_trie,
            documents: serializable.documents,
            doc_metadata: serializable.doc_metadata,
            token_offsets: serializable.token_offsets,
            tokenizer: Tokenizer::new(),
        })
    }
}

impl Default for SearchEngine {
    fn default() -> Self {
        Self::new()
    }
}
