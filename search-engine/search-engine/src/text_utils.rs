use regex::Regex;

/// Remove punctuation, keeping only Unicode letters and spaces.
/// Matches the Python `remove_punctuation` from `odrednice/text.py`.
pub fn remove_punctuation(text: &str) -> String {
    text.chars()
        .filter(|c| c.is_alphabetic() || *c == ' ')
        .collect()
}

/// Transliterate Serbian Cyrillic to Latin script.
/// Matches the Python `cyr_to_lat` from `pretraga/cyrlat.py`.
pub fn cyr_to_lat(text: &str) -> String {
    let mut result = text.to_string();

    // Multi-char mappings first (digraphs)
    result = result
        .replace('\u{0409}', "Lj")
        .replace('\u{040A}', "Nj")
        .replace('\u{040F}', "D\u{017E}")
        .replace('\u{0459}', "lj")
        .replace('\u{045A}', "nj")
        .replace('\u{045F}', "d\u{017E}");

    // Single-char mappings
    let cyrillic: &[char] = &[
        '\u{0410}', '\u{0411}', '\u{0412}', '\u{0413}',
        '\u{0414}', '\u{0402}', '\u{0415}', '\u{0416}', '\u{0417}', '\u{0418}',
        '\u{0408}', '\u{041A}', '\u{041B}', '\u{041C}', '\u{041D}', '\u{041E}',
        '\u{041F}', '\u{0420}', '\u{0421}', '\u{0422}', '\u{040B}', '\u{0423}',
        '\u{0424}', '\u{0425}', '\u{0426}', '\u{0427}', '\u{0428}', '\u{0430}',
        '\u{0431}', '\u{0432}', '\u{0433}', '\u{0434}', '\u{0452}', '\u{0435}',
        '\u{0436}', '\u{0437}', '\u{0438}', '\u{0458}', '\u{043A}', '\u{043B}',
        '\u{043C}', '\u{043D}', '\u{043E}', '\u{043F}', '\u{0440}', '\u{0441}',
        '\u{0442}', '\u{045B}', '\u{0443}', '\u{0444}', '\u{0445}', '\u{0446}',
        '\u{0447}', '\u{0448}',
    ];

    let latin: &[&str] = &[
        "A", "B", "V", "G", "D", "\u{0110}", "E",
        "\u{017D}", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S",
        "T", "\u{0106}", "U", "F", "H", "C", "\u{010C}", "\u{0160}", "a", "b",
        "v", "g", "d", "\u{0111}", "e", "\u{017E}", "z", "i", "j", "k", "l",
        "m", "n", "o", "p", "r", "s", "t", "\u{0107}", "u", "f", "h", "c",
        "\u{010D}", "\u{0161}",
    ];

    for (c, l) in cyrillic.iter().zip(latin.iter()) {
        result = result.replace(*c, l);
    }

    result
}

/// Expand parenthesized variants in a word.
/// E.g. "бе(с)крајан" -> ["бекрајан", "бескрајан"]
fn expand_parentheses(text: &str) -> Vec<String> {
    let re = Regex::new(r"^(.+)\((.*?)\)(.*?)$").unwrap();
    if let Some(caps) = re.captures(text) {
        let before = &caps[1];
        let inside = &caps[2];
        let after = &caps[3];
        vec![
            format!("{}{}", before, after),
            format!("{}{}{}", before, inside, after),
        ]
    } else {
        vec![text.to_string()]
    }
}

/// Prepare all searchable variants for a dictionary entry.
/// Collects rec + ijekavski + variant texts, expands parentheses,
/// removes punctuation, adds Latin transliterations, and deduplicates.
pub fn prepare_variants(
    rec: &str,
    ijekavski: Option<&str>,
    variant_texts: &[(Option<String>, Option<String>)], // (tekst, ijekavski) pairs
) -> Vec<String> {
    let mut raw: Vec<String> = Vec::new();

    raw.push(rec.to_string());
    if let Some(ij) = ijekavski {
        if !ij.is_empty() {
            raw.push(ij.to_string());
        }
    }
    for (tekst, ij) in variant_texts {
        if let Some(t) = tekst {
            if !t.is_empty() {
                raw.push(t.clone());
            }
        }
        if let Some(i) = ij {
            if !i.is_empty() {
                raw.push(i.clone());
            }
        }
    }

    // Expand parentheses and clean
    let mut cleaned: Vec<String> = Vec::new();
    for item in &raw {
        let expanded = expand_parentheses(item);
        for e in expanded {
            let c = remove_punctuation(&e);
            if !c.is_empty() && !cleaned.contains(&c) {
                cleaned.push(c);
            }
        }
    }

    // Add Latin transliterations
    let mut with_latin: Vec<String> = cleaned.clone();
    for item in &cleaned {
        let lat = cyr_to_lat(item);
        if !with_latin.contains(&lat) {
            with_latin.push(lat);
        }
    }

    with_latin
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_remove_punctuation() {
        assert_eq!(remove_punctuation("а̀бсурд"), "абсурд");
        assert_eq!(remove_punctuation("hello-world"), "helloworld");
        assert_eq!(remove_punctuation("реч."), "реч");
        assert_eq!(remove_punctuation("two words"), "two words");
    }

    #[test]
    fn test_cyr_to_lat() {
        assert_eq!(cyr_to_lat("абсурд"), "absurd");
        assert_eq!(cyr_to_lat("Београд"), "Beograd");
        assert_eq!(cyr_to_lat("љубав"), "ljubav");
        assert_eq!(cyr_to_lat("Њујорк"), "Njujork");
    }

    #[test]
    fn test_expand_parentheses() {
        let result = expand_parentheses("бе(с)крајан");
        assert_eq!(result, vec!["бекрајан", "бескрајан"]);

        let result = expand_parentheses("абсурд");
        assert_eq!(result, vec!["абсурд"]);
    }

    #[test]
    fn test_prepare_variants() {
        let variants = prepare_variants(
            "абсурд",
            None,
            &[],
        );
        assert!(variants.contains(&"абсурд".to_string()));
        assert!(variants.contains(&"absurd".to_string()));
    }

    #[test]
    fn test_prepare_variants_with_ijekavski() {
        let variants = prepare_variants(
            "млеко",
            Some("млијеко"),
            &[],
        );
        assert!(variants.contains(&"млеко".to_string()));
        assert!(variants.contains(&"млијеко".to_string()));
        assert!(variants.contains(&"mleko".to_string()));
        assert!(variants.contains(&"mlijeko".to_string()));
    }
}
