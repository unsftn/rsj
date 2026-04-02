use regex::Regex;

pub struct Tokenizer {
    word_pattern: Regex,
}

impl Tokenizer {
    pub fn new() -> Self {
        Self {
            word_pattern: Regex::new(r"\b\w+\b").unwrap(),
        }
    }

    pub fn tokenize(&self, text: &str) -> Vec<String> {
        self.word_pattern
            .find_iter(text)
            .map(|m| m.as_str().to_lowercase())
            .collect()
    }

    pub fn tokenize_with_positions(&self, text: &str) -> Vec<(String, usize)> {
        self.word_pattern
            .find_iter(text)
            .map(|m| (m.as_str().to_lowercase(), m.start()))
            .collect()
    }

    /// Returns (byte_start, byte_len) for each token — compact offset data
    /// suitable for caching without storing token strings.
    pub fn tokenize_offsets(&self, text: &str) -> Vec<(u32, u16)> {
        self.word_pattern
            .find_iter(text)
            .map(|m| (m.start() as u32, m.as_str().len() as u16))
            .collect()
    }
}

impl Default for Tokenizer {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tokenize() {
        let tokenizer = Tokenizer::new();
        let tokens = tokenizer.tokenize("Hello, World! This is a test.");
        assert_eq!(
            tokens,
            vec!["hello", "world", "this", "is", "a", "test"]
        );
    }

    #[test]
    fn test_tokenize_with_positions() {
        let tokenizer = Tokenizer::new();
        let text = "Hello World";
        let tokens = tokenizer.tokenize_with_positions(text);
        
        assert_eq!(tokens.len(), 2);
        assert_eq!(tokens[0], ("hello".to_string(), 0));
        assert_eq!(tokens[1], ("world".to_string(), 6));
    }
}
