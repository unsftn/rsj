use clap::{Parser, Subcommand};
use search_engine::{DocumentMetadata, SearchEngine, MorphologyEngine, OdrednicaEngine, NaslovEngine, WordType};
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "search-cli")]
#[command(about = "Document search engine CLI", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add a document to the index
    Add {
        /// Document ID
        #[arg(short, long)]
        id: i32,

        /// Path to document file
        #[arg(short, long)]
        file: PathBuf,

        /// Document title
        #[arg(short, long)]
        title: Option<String>,

        /// Document author
        #[arg(short, long)]
        author: Option<String>,

        /// Index file path
        #[arg(long, default_value = "data/search_index.bin")]
        index: PathBuf,
    },

    /// Save the index
    Save {
        /// Output index file path
        #[arg(short, long, default_value = "data/search_index.bin")]
        output: PathBuf,
    },

    /// Load the index
    Load {
        /// Input index file path
        #[arg(short, long, default_value = "data/search_index.bin")]
        input: PathBuf,
    },

    /// Show index statistics
    Stats {
        /// Index file path
        #[arg(long, default_value = "data/search_index.bin")]
        index: PathBuf,
    },

    /// Reindex documents from MySQL database
    Reindex {
        /// Database host
        #[arg(long)]
        host: String,

        /// Database port
        #[arg(long, default_value = "3306")]
        port: u16,

        /// Database name
        #[arg(long)]
        database: String,

        /// Database user
        #[arg(long)]
        user: String,

        /// Database password
        #[arg(long)]
        password: String,

        /// Force reindex (overwrite existing)
        #[arg(long)]
        force: bool,

        /// Limit number of documents (for testing)
        #[arg(long)]
        limit: Option<usize>,

        /// Output index file path
        #[arg(long, default_value = "search_index/search_index.bin")]
        output: PathBuf,
    },

    /// Add a word to the morphology dictionary
    MorphAdd {
        /// Base form of the word
        #[arg(short, long)]
        base: String,

        /// Word type (noun, verb, adjective, etc.)
        #[arg(short = 't', long)]
        word_type: String,

        /// Grammatical forms (comma-separated)
        #[arg(short, long)]
        forms: String,

        /// Morphology dictionary file path
        #[arg(long, default_value = "search_index/morphology.bin")]
        dict: PathBuf,
    },

    /// Show morphology dictionary statistics
    MorphStats {
        /// Morphology dictionary file path
        #[arg(long, default_value = "search_index/morphology.bin")]
        dict: PathBuf,
    },

    /// Search for words by form
    MorphSearch {
        /// Word form to search for
        #[arg(short, long)]
        form: String,

        /// Morphology dictionary file path
        #[arg(long, default_value = "search_index/morphology.bin")]
        dict: PathBuf,
    },

    /// Search for words by prefix (autocomplete)
    MorphPrefix {
        /// Prefix to search for
        #[arg(short, long)]
        prefix: String,

        /// Maximum results
        #[arg(short, long, default_value = "10")]
        limit: usize,

        /// Morphology dictionary file path
        #[arg(long, default_value = "search_index/morphology.bin")]
        dict: PathBuf,
    },

    /// Import dictionary entries (odrednice) from MySQL database
    OdrImport {
        /// Database host
        #[arg(long)]
        host: String,

        /// Database port
        #[arg(long, default_value = "3306")]
        port: u16,

        /// Database name
        #[arg(long)]
        database: String,

        /// Database user
        #[arg(long)]
        user: String,

        /// Database password
        #[arg(long)]
        password: String,

        /// Force import (overwrite existing)
        #[arg(long)]
        force: bool,

        /// Limit number of entries (for testing)
        #[arg(long)]
        limit: Option<usize>,

        /// Output odrednica dictionary file path
        #[arg(long, default_value = "search_index/odrednica.bin")]
        output: PathBuf,
    },

    /// Show odrednica dictionary statistics
    OdrStats {
        /// Odrednica dictionary file path
        #[arg(long, default_value = "search_index/odrednica.bin")]
        dict: PathBuf,
    },

    /// Import publication titles/descriptions from MySQL database
    NaslovImport {
        /// Database host
        #[arg(long)]
        host: String,

        /// Database port
        #[arg(long, default_value = "3306")]
        port: u16,

        /// Database name
        #[arg(long)]
        database: String,

        /// Database user
        #[arg(long)]
        user: String,

        /// Database password
        #[arg(long)]
        password: String,

        /// Force import (overwrite existing)
        #[arg(long)]
        force: bool,

        /// Output naslov index file path
        #[arg(long, default_value = "search_index/naslov.bin")]
        output: PathBuf,
    },

    /// Show naslov index statistics
    NaslovStats {
        /// Naslov index file path
        #[arg(long, default_value = "search_index/naslov.bin")]
        dict: PathBuf,
    },

    /// Import all indexes from both recnik and korpus databases
    ImportAll {
        /// Recnik database host
        #[arg(long, default_value = "localhost")]
        recnik_host: String,

        /// Recnik database port
        #[arg(long, default_value = "3306")]
        recnik_port: u16,

        /// Recnik database name
        #[arg(long, default_value = "recnik")]
        recnik_database: String,

        /// Recnik database user
        #[arg(long, default_value = "recnik")]
        recnik_user: String,

        /// Recnik database password
        #[arg(long, default_value = "recnik")]
        recnik_password: String,

        /// Korpus database host
        #[arg(long, default_value = "localhost")]
        korpus_host: String,

        /// Korpus database port
        #[arg(long, default_value = "3306")]
        korpus_port: u16,

        /// Korpus database name
        #[arg(long, default_value = "korpus")]
        korpus_database: String,

        /// Korpus database user
        #[arg(long, default_value = "korpus")]
        korpus_user: String,

        /// Korpus database password
        #[arg(long, default_value = "korpus")]
        korpus_password: String,

        /// Force import (overwrite existing)
        #[arg(long)]
        force: bool,

        /// Output directory for index files
        #[arg(long, default_value = "search_index")]
        output_dir: PathBuf,
    },

    /// Import words from MySQL database into morphology dictionary
    MorphImport {
        /// Database host
        #[arg(long)]
        host: String,

        /// Database port
        #[arg(long, default_value = "3306")]
        port: u16,

        /// Database name
        #[arg(long)]
        database: String,

        /// Database user
        #[arg(long)]
        user: String,

        /// Database password
        #[arg(long)]
        password: String,

        /// Force import (overwrite existing)
        #[arg(long)]
        force: bool,

        /// Limit number of words (for testing)
        #[arg(long)]
        limit: Option<usize>,

        /// Output morphology dictionary file path
        #[arg(long, default_value = "search_index/morphology.bin")]
        output: PathBuf,
    },
}

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Add { id, file, title, author, index } => {
            cmd_add(id, &file, title, author, &index)?;
        }
        Commands::Save { output } => {
            cmd_save(&output)?;
        }
        Commands::Load { input } => {
            cmd_load(&input)?;
        }
        Commands::Stats { index } => {
            cmd_stats(&index)?;
        }
        Commands::Reindex {
            host,
            port,
            database,
            user,
            password,
            force,
            limit,
            output,
        } => {
            cmd_reindex(&host, port, &database, &user, &password, force, limit, &output)?;
        }
        Commands::MorphAdd { base, word_type, forms, dict } => {
            cmd_morph_add(&base, &word_type, &forms, &dict)?;
        }
        Commands::MorphStats { dict } => {
            cmd_morph_stats(&dict)?;
        }
        Commands::MorphSearch { form, dict } => {
            cmd_morph_search(&form, &dict)?;
        }
        Commands::MorphPrefix { prefix, limit, dict } => {
            cmd_morph_prefix(&prefix, limit, &dict)?;
        }
        Commands::ImportAll {
            recnik_host,
            recnik_port,
            recnik_database,
            recnik_user,
            recnik_password,
            korpus_host,
            korpus_port,
            korpus_database,
            korpus_user,
            korpus_password,
            force,
            output_dir,
        } => {
            cmd_import_all(
                &recnik_host, recnik_port, &recnik_database, &recnik_user, &recnik_password,
                &korpus_host, korpus_port, &korpus_database, &korpus_user, &korpus_password,
                force, &output_dir,
            )?;
        }
        Commands::MorphImport {
            host,
            port,
            database,
            user,
            password,
            force,
            limit,
            output,
        } => {
            cmd_morph_import(&host, port, &database, &user, &password, force, limit, &output)?;
        }
        Commands::OdrImport {
            host,
            port,
            database,
            user,
            password,
            force,
            limit,
            output,
        } => {
            cmd_odr_import(&host, port, &database, &user, &password, force, limit, &output)?;
        }
        Commands::OdrStats { dict } => {
            cmd_odr_stats(&dict)?;
        }
        Commands::NaslovImport {
            host,
            port,
            database,
            user,
            password,
            force,
            output,
        } => {
            cmd_naslov_import(&host, port, &database, &user, &password, force, &output)?;
        }
        Commands::NaslovStats { dict } => {
            cmd_naslov_stats(&dict)?;
        }
    }

    Ok(())
}

fn cmd_import_all(
    recnik_host: &str,
    recnik_port: u16,
    recnik_database: &str,
    recnik_user: &str,
    recnik_password: &str,
    korpus_host: &str,
    korpus_port: u16,
    korpus_database: &str,
    korpus_user: &str,
    korpus_password: &str,
    force: bool,
    output_dir: &PathBuf,
) -> anyhow::Result<()> {
    use std::time::Instant;

    println!("================================================================================");
    println!("IMPORT ALL INDEXES");
    println!("================================================================================");
    println!("Recnik DB:  {}@{}:{}/{}", recnik_user, recnik_host, recnik_port, recnik_database);
    println!("Korpus DB:  {}@{}:{}/{}", korpus_user, korpus_host, korpus_port, korpus_database);
    println!("Output dir: {:?}", output_dir);
    println!("Force:      {}", force);
    println!("================================================================================\n");

    if !output_dir.exists() {
        std::fs::create_dir_all(output_dir)?;
        println!("✓ Created output directory: {:?}\n", output_dir);
    }

    let total_start = Instant::now();
    let mut step = 1;

    // Step 1: Morphology import (from korpus database)
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("Step {}: Morphology import (from korpus)", step);
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    let morph_output = output_dir.join("morphology.bin");
    let start = Instant::now();
    cmd_morph_import(korpus_host, korpus_port, korpus_database, korpus_user, korpus_password, force, None, &morph_output)?;
    println!("✓ Morphology import completed in {:?}\n", start.elapsed());
    step += 1;

    // Step 2: Odrednica import (from recnik database)
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("Step {}: Odrednica import (from recnik)", step);
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    let odr_output = output_dir.join("odrednica.bin");
    let start = Instant::now();
    cmd_odr_import(recnik_host, recnik_port, recnik_database, recnik_user, recnik_password, force, None, &odr_output)?;
    println!("✓ Odrednica import completed in {:?}\n", start.elapsed());
    step += 1;

    // Step 3: Naslov import (from korpus database)
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("Step {}: Naslov import (from korpus)", step);
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    let naslov_output = output_dir.join("naslov.bin");
    let start = Instant::now();
    cmd_naslov_import(korpus_host, korpus_port, korpus_database, korpus_user, korpus_password, force, &naslov_output)?;
    println!("✓ Naslov import completed in {:?}\n", start.elapsed());
    step += 1;

    // Step 4: Full-text reindex (from korpus database)
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("Step {}: Full-text reindex (from korpus)", step);
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    let search_output = output_dir.join("search_index.bin");
    let start = Instant::now();
    cmd_reindex(korpus_host, korpus_port, korpus_database, korpus_user, korpus_password, force, None, &search_output)?;
    println!("✓ Full-text reindex completed in {:?}\n", start.elapsed());

    println!("================================================================================");
    println!("ALL IMPORTS COMPLETED in {:?}", total_start.elapsed());
    println!("================================================================================");
    println!("Output files:");
    println!("  Morphology:  {:?}", output_dir.join("morphology.bin"));
    println!("  Odrednica:   {:?}", output_dir.join("odrednica.bin"));
    println!("  Naslov:      {:?}", output_dir.join("naslov.bin"));
    println!("  Full-text:   {:?}", output_dir.join("search_index.bin"));

    Ok(())
}

fn cmd_add(
    doc_id: i32,
    file_path: &PathBuf,
    title: Option<String>,
    author: Option<String>,
    index_path: &PathBuf,
) -> anyhow::Result<()> {
    let text = std::fs::read_to_string(file_path)?;

    let mut engine = if index_path.exists() {
        println!("✓ Loading existing index from {:?}", index_path);
        SearchEngine::load(index_path)?
    } else {
        println!("ℹ Creating new index");
        SearchEngine::new()
    };

    let metadata = DocumentMetadata { title, author };
    engine.add_document(doc_id, text, metadata);

    println!("✓ Added document: {}", doc_id);

    engine.save(index_path)?;
    println!("✓ Index saved to {:?}", index_path);

    let stats = engine.get_stats();
    println!("\nStatistics:");
    for (key, value) in stats {
        println!("  {}: {}", key, value);
    }

    Ok(())
}

fn cmd_save(_output_path: &PathBuf) -> anyhow::Result<()> {
    println!("✗ No engine loaded. Use 'add' or 'reindex' commands instead.");
    Ok(())
}

fn cmd_load(input_path: &PathBuf) -> anyhow::Result<()> {
    let engine = SearchEngine::load(input_path)?;
    println!("✓ Index loaded from {:?}", input_path);

    let stats = engine.get_stats();
    println!("\nStatistics:");
    for (key, value) in stats {
        println!("  {}: {}", key, value);
    }

    Ok(())
}

fn cmd_stats(index_path: &PathBuf) -> anyhow::Result<()> {
    if !index_path.exists() {
        println!("✗ Index file not found: {:?}", index_path);
        return Ok(());
    }

    let engine = SearchEngine::load(index_path)?;
    let stats = engine.get_stats();

    println!("\n=== Search Engine Statistics ===");
    for (key, value) in stats {
        println!("{}: {}", key, value);
    }

    Ok(())
}

fn cmd_reindex(
    host: &str,
    port: u16,
    database: &str,
    user: &str,
    password: &str,
    force: bool,
    limit: Option<usize>,
    output_path: &PathBuf,
) -> anyhow::Result<()> {
    use mysql::prelude::*;
    use mysql::*;
    use std::time::Instant;

    // Check if index exists
    if output_path.exists() && !force {
        println!("✗ Index already exists at {:?}", output_path);
        println!("  Use --force to overwrite");
        return Ok(());
    }

    if output_path.exists() && force {
        println!("⚠ Removing existing index at {:?}", output_path);
        std::fs::remove_file(output_path)?;
    }

    println!("================================================================================");
    println!("DATABASE REINDEXING");
    println!("================================================================================");
    println!("Database: {}@{}:{}", database, host, port);
    println!("Output:   {:?}", output_path);
    println!("================================================================================\n");

    // Connect to database
    println!("→ Connecting to database...");
    let url = format!("mysql://{}:{}@{}:{}/{}", user, password, host, port, database);
    let pool = Pool::new(url.as_str())?;
    let mut conn = pool.get_conn()?;
    println!("✓ Connected to database\n");

    // Count documents
    println!("→ Counting documents...");
    let count: i64 = conn.query_first("SELECT COUNT(*) FROM publikacije_publikacija")?.unwrap_or(0);
    let total_docs = if let Some(lim) = limit {
        count.min(lim as i64)
    } else {
        count
    };
    println!("✓ Found {} documents\n", total_docs);

    // Create search engine
    let mut engine = SearchEngine::new();

    println!("→ Indexing documents...");
    let start_time = Instant::now();

    let query = if let Some(lim) = limit {
        format!("SELECT id, naslov FROM publikacije_publikacija LIMIT {}", lim)
    } else {
        "SELECT id, naslov FROM publikacije_publikacija".to_string()
    };

    let documents: Vec<(i32, Option<String>)> = conn.query(query)?;

    let mut count = 0;
    let mut skipped = 0;

    for (doc_id, title) in documents {
        // Fetch text fragments
        let texts: Vec<(i32, i32, Option<String>)> = conn.exec(
            "SELECT id, redni_broj, tekst FROM publikacije_tekstpublikacije WHERE publikacija_id = ? ORDER BY redni_broj",
            (doc_id,)
        )?;

        let mut text_parts = Vec::new();
        for (_text_id, _redni_broj, tekst) in texts {
            if let Some(t) = tekst {
                text_parts.push(t);
            }
        }

        let text = text_parts.join(" ");

        if !text.is_empty() {
            let metadata = DocumentMetadata {
                title: title.or_else(|| Some(format!("Document {}", doc_id))),
                author: None,
            };
            engine.add_document(doc_id, text, metadata);
            count += 1;
        } else {
            skipped += 1;
        }

        if (count + skipped) % 1000 == 0 {
            let elapsed = start_time.elapsed().as_secs_f64();
            let docs_per_sec = (count + skipped) as f64 / elapsed;
            let eta_seconds = (total_docs - count - skipped) as f64 / docs_per_sec;

            println!(
                "  Progress: {}/{} ({:.1}%) | Speed: {:.1} docs/sec | ETA: {:.1} min",
                count + skipped,
                total_docs,
                100.0 * (count + skipped) as f64 / total_docs as f64,
                docs_per_sec,
                eta_seconds / 60.0
            );
        }
    }

    println!("\n✓ Indexed {} documents ({} skipped - no content)", count, skipped);

    // Save index
    println!("\n→ Saving index to disk...");
    println!("NOTE: If stack overflow occurs, run with: RUST_MIN_STACK=33554432 ./search-cli reindex ...");
    let save_start = Instant::now();
    engine.save(output_path)?;
    let save_time = save_start.elapsed();
    println!("✓ Index saved in {:.2} seconds", save_time.as_secs_f64());

    // Final statistics
    let total_time = start_time.elapsed();
    let stats = engine.get_stats();

    println!("\n================================================================================");
    println!("INDEXING COMPLETE");
    println!("================================================================================");
    println!("Total time:       {:.2} seconds ({:.2} minutes)", total_time.as_secs_f64(), total_time.as_secs_f64() / 60.0);
    println!("Documents:        {}", stats.get("num_documents").unwrap_or(&"0".to_string()));
    println!("Vocabulary:       {} unique words", stats.get("vocabulary_size").unwrap_or(&"0".to_string()));
    println!("Total characters: {}", stats.get("total_chars").unwrap_or(&"0".to_string()));
    println!("Average speed:    {:.1} docs/sec", count as f64 / total_time.as_secs_f64());
    println!("Index file:       {:?}", output_path);

    if let Ok(metadata) = std::fs::metadata(output_path) {
        let size_mb = metadata.len() as f64 / (1024.0 * 1024.0);
        println!("Index size:       {:.2} MB", size_mb);
    }

    println!("================================================================================");

    Ok(())
}

fn cmd_morph_add(
    base: &str,
    word_type_str: &str,
    forms_str: &str,
    dict_path: &PathBuf,
) -> anyhow::Result<()> {
    let word_type = WordType::from_str(word_type_str);
    let forms: Vec<String> = forms_str.split(',').map(|s| s.trim().to_string()).collect();

    let mut engine = if dict_path.exists() {
        println!("✓ Loading existing dictionary from {:?}", dict_path);
        MorphologyEngine::load(dict_path)?
    } else {
        println!("ℹ Creating new dictionary");
        MorphologyEngine::new()
    };

    let word_id = engine.add_word(base.to_string(), word_type.clone(), forms.clone());

    println!("✓ Added word: {} (ID: {}, type: {})", base, word_id, word_type.to_string());
    println!("  Forms: {}", forms.join(", "));

    engine.save(dict_path)?;
    println!("✓ Dictionary saved to {:?}", dict_path);

    Ok(())
}

fn cmd_morph_stats(dict_path: &PathBuf) -> anyhow::Result<()> {
    if !dict_path.exists() {
        println!("✗ Dictionary file not found: {:?}", dict_path);
        return Ok(());
    }

    let engine = MorphologyEngine::load(dict_path)?;
    let stats = engine.get_stats();

    println!("\n=== Morphology Dictionary Statistics ===");
    for (key, value) in stats {
        println!("{}: {}", key, value);
    }

    Ok(())
}

fn cmd_morph_search(form: &str, dict_path: &PathBuf) -> anyhow::Result<()> {
    if !dict_path.exists() {
        println!("✗ Dictionary file not found: {:?}", dict_path);
        return Ok(());
    }

    let engine = MorphologyEngine::load(dict_path)?;
    let results = engine.search_by_form(form);

    if results.is_empty() {
        println!("No words found for form: {}", form);
    } else {
        println!("Found {} word(s) for form '{}':\n", results.len(), form);
        for word in results {
            let orig_id_str = word.original_id
                .map(|id| format!(" [DB ID: {}]", id))
                .unwrap_or_default();
            println!("  [ID: {}]{} {} ({})", word.id, orig_id_str, word.base_form, word.word_type.to_string());
            println!("    Forms: {}", word.forms.join(", "));
            println!();
        }
    }

    Ok(())
}

fn cmd_morph_prefix(prefix: &str, limit: usize, dict_path: &PathBuf) -> anyhow::Result<()> {
    if !dict_path.exists() {
        println!("✗ Dictionary file not found: {:?}", dict_path);
        return Ok(());
    }

    let engine = MorphologyEngine::load(dict_path)?;
    let results = engine.search_by_prefix(prefix);

    if results.is_empty() {
        println!("No words found with prefix: {}", prefix);
    } else {
        let display_count = results.len().min(limit);
        println!("Found {} word(s) with prefix '{}' (showing {}):\n",
                 results.len(), prefix, display_count);

        for word in results.iter().take(limit) {
            let orig_id_str = word.original_id
                .map(|id| format!(" [DB ID: {}]", id))
                .unwrap_or_default();
            println!("  [ID: {}]{} {} ({})", word.id, orig_id_str, word.base_form, word.word_type.to_string());
            println!("    Forms: {}", word.forms.join(", "));
            println!();
        }

        if results.len() > limit {
            println!("... and {} more", results.len() - limit);
        }
    }

    Ok(())
}

fn cmd_morph_import(
    host: &str,
    port: u16,
    database: &str,
    user: &str,
    password: &str,
    force: bool,
    limit: Option<usize>,
    output_path: &PathBuf,
) -> anyhow::Result<()> {
    use mysql::prelude::*;
    use mysql::*;
    use std::time::Instant;

    // Check if dictionary exists
    if output_path.exists() && !force {
        println!("✗ Dictionary already exists at {:?}", output_path);
        println!("  Use --force to overwrite");
        return Ok(());
    }

    if output_path.exists() && force {
        println!("⚠ Removing existing dictionary at {:?}", output_path);
        std::fs::remove_file(output_path)?;
    }

    println!("================================================================================");
    println!("MORPHOLOGY DICTIONARY IMPORT");
    println!("================================================================================");
    println!("Database: {}@{}:{}", database, host, port);
    println!("Output:   {:?}", output_path);
    println!("================================================================================\n");

    // Connect to database
    let url = format!("mysql://{}:{}@{}:{}/{}", user, password, host, port, database);
    let pool = Pool::new(url.as_str())?;
    let mut conn = pool.get_conn()?;
    println!("Connected to database\n");

    // Create morphology engine
    let mut engine = MorphologyEngine::new();

    // Define tables to process with their display names
    let tables_to_process = vec![
        ("reci_imenica", "imenice"),  // Use the provided table as the primary one
        ("reci_glagol", "glagoli"),
        ("reci_pridev", "pridevi"),
        ("reci_prilog", "prilozi"),
        ("reci_zamenica", "zamenice"),
        ("reci_predlog", "predlozi"),
        ("reci_veznik", "veznici"),
        ("reci_uzvik", "uzvici"),
        ("reci_recca", "recce"),
        ("reci_broj", "brojevi"),
    ];

    let start_time = Instant::now();
    let mut total_imported = 0;
    let mut total_skipped = 0;

    // Count words in each table
    for (table_name, display_name) in &tables_to_process {
        let count_query = format!("SELECT COUNT(*) FROM {}", table_name);
        let count: i64 = conn.query_first(&count_query)?.unwrap_or(0);
        let total_words_in_table = if let Some(lim) = limit {
            count.min(lim as i64)
        } else {
            count
        };
        println!("Found {} {} in table '{}'", total_words_in_table, display_name, table_name);
    }

    println!("Importing imenice...");
    let word_type = WordType::Imenica;

    let query = format!("SELECT id, nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed, nommno, genmno, datmno, akumno, vokmno, insmno, lokmno FROM reci_imenica");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let nomjed: Option<String> = row.get(1).unwrap();
        if nomjed.is_none() {
            total_skipped += 1;
            continue;
        }
        let genjed: Option<String> = row.get(2).unwrap();
        let datjed: Option<String> = row.get(3).unwrap();
        let akujed: Option<String> = row.get(4).unwrap();
        let vokjed: Option<String> = row.get(5).unwrap();
        let insjed: Option<String> = row.get(6).unwrap();
        let lokjed: Option<String> = row.get(7).unwrap();
        let nommno: Option<String> = row.get(8).unwrap();
        let genmno: Option<String> = row.get(9).unwrap();
        let datmno: Option<String> = row.get(10).unwrap();
        let akumno: Option<String> = row.get(11).unwrap();
        let vokmno: Option<String> = row.get(12).unwrap();
        let insmno: Option<String> = row.get(13).unwrap();
        let lokmno: Option<String> = row.get(14).unwrap();
        let base_form: String = nomjed.clone().unwrap();
        let mut forms: Vec<String> = Vec::new();
        let form_values: Vec<String> = vec![
            nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed,
            nommno, genmno, datmno, akumno, vokmno, insmno, lokmno
        ].into_iter().filter_map(|x| x).collect();

        for form in form_values {
            if !form.is_empty() && !forms.contains(&form) {
                forms.push(form);
            }
        }

        let query2 = format!("SELECT id, nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed, nommno, genmno, datmno, akumno, vokmno, insmno, lokmno FROM reci_varijantaimenice WHERE imenica_id={}", original_db_id);
        let rows2: Vec<Row> = conn.query(query2)?;
        for var_row in rows2 {
            let _v_id: i32 = var_row.get(0).unwrap();
            let v_nomjed: Option<String> = var_row.get(1).unwrap();
            let v_genjed: Option<String> = var_row.get(2).unwrap();
            let v_datjed: Option<String> = var_row.get(3).unwrap();
            let v_akujed: Option<String> = var_row.get(4).unwrap();
            let v_vokjed: Option<String> = var_row.get(5).unwrap();
            let v_insjed: Option<String> = var_row.get(6).unwrap();
            let v_lokjed: Option<String> = var_row.get(7).unwrap();
            let v_nommno: Option<String> = var_row.get(8).unwrap();
            let v_genmno: Option<String> = var_row.get(9).unwrap();
            let v_datmno: Option<String> = var_row.get(10).unwrap();
            let v_akumno: Option<String> = var_row.get(11).unwrap();
            let v_vokmno: Option<String> = var_row.get(12).unwrap();
            let v_insmno: Option<String> = var_row.get(13).unwrap();
            let v_lokmno: Option<String> = var_row.get(14).unwrap();
            let form_values2: Vec<String> = vec![
                v_nomjed, v_genjed, v_datjed, v_akujed, v_vokjed, v_insjed, v_lokjed,
                v_nommno, v_genmno, v_datmno, v_akumno, v_vokmno, v_insmno, v_lokmno
            ].into_iter().filter_map(|x| x).collect();

            for form in form_values2 {
                if !form.is_empty() && !forms.contains(&form) {
                    forms.push(form);
                }
            }
        }
        // Use auto-generated ID but preserve original database ID as metadata
        let _new_id = engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing glagoli...");
    let word_type = WordType::Glagol;
    let query = format!("SELECT id, infinitiv, gpp, gps, rgp_mj, rgp_mm, rgp_sj, rgp_sm, rgp_zj, rgp_zm, tgp_mj, tgp_mm, tgp_sj, tgp_sm, tgp_zj, tgp_zm, gpp2 FROM reci_glagol");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let infinitiv: Option<String> = row.get(1).unwrap();
        if infinitiv.is_none() {
            total_skipped += 1;
            continue;
        }
        let gpp: Option<String> = row.get(2).unwrap();
        let gps: Option<String> = row.get(3).unwrap();
        let rgp_mj: Option<String> = row.get(4).unwrap();
        let rgp_mm: Option<String> = row.get(5).unwrap();
        let rgp_sj: Option<String> = row.get(6).unwrap();
        let rgp_sm: Option<String> = row.get(7).unwrap();
        let rgp_zj: Option<String> = row.get(8).unwrap();
        let rgp_zm: Option<String> = row.get(9).unwrap();
        let tgp_mj: Option<String> = row.get(10).unwrap();
        let tgp_mm: Option<String> = row.get(11).unwrap();
        let tgp_sj: Option<String> = row.get(12).unwrap();
        let tgp_sm: Option<String> = row.get(13).unwrap();
        let tgp_zj: Option<String> = row.get(14).unwrap();
        let tgp_zm: Option<String> = row.get(15).unwrap();
        let gpp2: Option<String> = row.get(16).unwrap();
        let base_form: String = infinitiv.clone().unwrap();
        let mut forms: Vec<String> = Vec::new();
        let form_values: Vec<String> = vec![
            infinitiv, gpp, gps, rgp_mj, rgp_mm, rgp_sj, rgp_sm, rgp_zj, rgp_zm,
            tgp_mj, tgp_mm, tgp_sj, tgp_sm, tgp_zj, tgp_zm, gpp2
        ].into_iter().filter_map(|x| x).collect();
        for form in form_values {
            if !form.is_empty() && !forms.contains(&form) {
                forms.push(form);
            }
        }
        let query2 = format!("SELECT id, jd1, jd2, jd3, mn1, mn2, mn3 FROM reci_oblikglagola WHERE glagol_id={}", original_db_id);
        let rows2: Vec<Row> = conn.query(query2)?;
        for var_row in rows2 {
            let o_id: i32 = var_row.get(0).unwrap();
            let jd1: Option<String> = var_row.get(1).unwrap();
            let jd2: Option<String> = var_row.get(2).unwrap();
            let jd3: Option<String> = var_row.get(3).unwrap();
            let mn1: Option<String> = var_row.get(4).unwrap();
            let mn2: Option<String> = var_row.get(5).unwrap();
            let mn3: Option<String> = var_row.get(6).unwrap();
            let form_values2: Vec<String> = vec![
                jd1, jd2, jd3, mn1, mn2, mn3
            ].into_iter().filter_map(|x| x).collect();
            for form in form_values2 {
                if !form.is_empty() && !forms.contains(&form) {
                    forms.push(form);
                }
            }

            let query3 = format!("SELECT varijanta FROM reci_varijanteglagola WHERE oblik_glagola_id={}", o_id);
            let row3: Vec<Row> = conn.query(query3)?;
            for var3_row in row3 {
                let varijanta: Option<String> = var3_row.get(0).unwrap();
                if let Some(var_form) = varijanta {
                    if !var_form.is_empty() && !forms.contains(&var_form) {
                        forms.push(var_form);
                    }
                }
            }
        }
        // Use auto-generated ID but preserve original database ID as metadata
        let _new_id = engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing pridevi...");
    let word_type = WordType::Pridev;
    let query = format!("SELECT * FROM reci_pridev");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get("id").unwrap();
        let base_form: Option<String> = row.get("lema").unwrap();
        if base_form.is_none() {
            total_skipped += 1;
            continue;
        }
        let mut forms: Vec<String> = Vec::new();
        for i in 1..row.len() {
            let column_name = row.columns_ref()[i].name_str();
            if !column_name.starts_with("mk") &&
               !column_name.starts_with("mn") &&
               !column_name.starts_with("mo") &&
               !column_name.starts_with("ms") &&
               !column_name.starts_with("sk") &&
               !column_name.starts_with("sp") &&
               !column_name.starts_with("ss") &&
               !column_name.starts_with("zk") &&
               !column_name.starts_with("zp") &&
               !column_name.starts_with("zs") {
                continue;
            }
            let form: Option<String> = row.get(i).unwrap();
            if let Some(f) = form {
                if !f.trim().is_empty() && !forms.contains(&f) {
                    forms.push(f);
                }
            }
        }
        let query2 = format!("SELECT * FROM reci_varijantaprideva WHERE pridev_id={}", original_db_id);
        let rows2: Vec<Row> = conn.query(query2)?;
        for var_row in rows2 {
            let _v_id: i32 = var_row.get("id").unwrap();
            for i in 1..var_row.len() {
                let column_name = var_row.columns_ref()[i].name_str();
                if column_name == "id" ||
                   column_name == "pridev_id" ||
                   column_name == "rod" ||
                   column_name == "redni_broj" {
                    continue;
                }
                let form: Option<String> = var_row.get(i).unwrap();
                if let Some(f) = form {
                    if !f.trim().is_empty() && !forms.contains(&f) {
                        forms.push(f);
                    }
                }
            }
        }
        let base_form: String = base_form.clone().unwrap();
        // Use auto-generated ID but preserve original database ID as metadata
        let _new_id = engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing zamenice...");
    let word_type = WordType::Zamenica;
    let query = format!("SELECT id, nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed FROM reci_zamenica");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let nomjed: Option<String> = row.get(1).unwrap();
        if nomjed.is_none() {
            total_skipped += 1;
            continue;
        }
        let genjed: Option<String> = row.get(2).unwrap();
        let datjed: Option<String> = row.get(3).unwrap();
        let akujed: Option<String> = row.get(4).unwrap();
        let vokjed: Option<String> = row.get(5).unwrap();
        let insjed: Option<String> = row.get(6).unwrap();
        let lokjed: Option<String> = row.get(7).unwrap();
        let base_form: String = nomjed.clone().unwrap();
        let mut forms: Vec<String> = Vec::new();
        let form_values: Vec<String> = vec![
            nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed
        ].into_iter().filter_map(|x| x).collect();
        for form in form_values {
            if !form.is_empty() && !forms.contains(&form) {
                forms.push(form);
            }
        }

        let query2 = format!("SELECT nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed FROM reci_varijantazamenice WHERE zamenica_id={}", original_db_id);
        let rows2: Vec<Row> = conn.query(query2)?;
        for var_row in rows2 {
            let v_nomjed: Option<String> = var_row.get(0).unwrap();
            let v_genjed: Option<String> = var_row.get(1).unwrap();
            let v_datjed: Option<String> = var_row.get(2).unwrap();
            let v_akujed: Option<String> = var_row.get(3).unwrap();
            let v_vokjed: Option<String> = var_row.get(4).unwrap();
            let v_insjed: Option<String> = var_row.get(5).unwrap();
            let v_lokjed: Option<String> = var_row.get(6).unwrap();
            let form_values2: Vec<String> = vec![
                v_nomjed, v_genjed, v_datjed, v_akujed, v_vokjed, v_insjed, v_lokjed
            ].into_iter().filter_map(|x| x).collect();
            for form in form_values2 {
                if !form.is_empty() && !forms.contains(&form) {
                    forms.push(form);
                }
            }
        }

        engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing prilozi...");
    let word_type = WordType::Prilog;
    let query = format!("SELECT id, pozitiv, komparativ, superlativ FROM reci_prilog");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let pozitiv: Option<String> = row.get(1).unwrap();
        if pozitiv.is_none() {
            total_skipped += 1;
            continue;
        }
        let komparativ: Option<String> = row.get(2).unwrap();
        let superlativ: Option<String> = row.get(3).unwrap();
        let base_form: String = pozitiv.clone().unwrap();
        let mut forms: Vec<String> = Vec::new();
        let form_values: Vec<String> = vec![
            pozitiv, komparativ, superlativ
        ].into_iter().filter_map(|x| x).collect();
        for form in form_values {
            if !form.is_empty() && !forms.contains(&form) {
                forms.push(form);
            }
        }
        engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing uzvici...");
    let word_type = WordType::Uzvik;
    let query = format!("SELECT id, tekst FROM reci_uzvik");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let tekst: Option<String> = row.get(1).unwrap();
        if tekst.is_none() {
            total_skipped += 1;
            continue;
        }
        let base_form: String = tekst.clone().unwrap();
        let forms: Vec<String> = vec![base_form.clone()];
        engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing recce...");
    let word_type = WordType::Recca;
    let query = format!("SELECT id, tekst FROM reci_recca");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let tekst: Option<String> = row.get(1).unwrap();
        if tekst.is_none() {
            total_skipped += 1;
            continue;
        }
        let base_form: String = tekst.clone().unwrap();
        let forms: Vec<String> = vec![base_form.clone()];
        engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing brojevi...");
    let word_type = WordType::Broj;
    let query = format!("SELECT id, nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed, nommno, genmno, datmno, akumno, vokmno, insmno, lokmno FROM reci_broj");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let nomjed: Option<String> = row.get(1).unwrap();
        if nomjed.is_none() {
            total_skipped += 1;
            continue;
        }
        let genjed: Option<String> = row.get(2).unwrap();
        let datjed: Option<String> = row.get(3).unwrap();
        let akujed: Option<String> = row.get(4).unwrap();
        let vokjed: Option<String> = row.get(5).unwrap();
        let insjed: Option<String> = row.get(6).unwrap();
        let lokjed: Option<String> = row.get(7).unwrap();
        let nommno: Option<String> = row.get(8).unwrap();
        let genmno: Option<String> = row.get(9).unwrap();
        let datmno: Option<String> = row.get(10).unwrap();
        let akumno: Option<String> = row.get(11).unwrap();
        let vokmno: Option<String> = row.get(12).unwrap();
        let insmno: Option<String> = row.get(13).unwrap();
        let lokmno: Option<String> = row.get(14).unwrap();
        let base_form: String = nomjed.clone().unwrap();
        let mut forms: Vec<String> = Vec::new();
        let form_values: Vec<String> = vec![
            nomjed, genjed, datjed, akujed, vokjed, insjed, lokjed,
            nommno, genmno, datmno, akumno, vokmno, insmno, lokmno
        ].into_iter().filter_map(|x| x).collect();
        for form in form_values {
            if !form.is_empty() && !forms.contains(&form) {
                forms.push(form);
            }
        }
        engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing predlozi...");
    let word_type = WordType::Predlog;
    let query = format!("SELECT id, tekst FROM reci_predlog");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let tekst: Option<String> = row.get(1).unwrap();
        if tekst.is_none() {
            total_skipped += 1;
            continue;
        }
        let base_form: String = tekst.clone().unwrap();
        let forms: Vec<String> = vec![base_form.clone()];
        engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Importing veznici...");
    let word_type = WordType::Veznik;
    let query = format!("SELECT id, tekst FROM reci_veznik");
    let rows: Vec<Row> = conn.query(query)?;
    for row in rows {
        let original_db_id: i32 = row.get(0).unwrap();
        let tekst: Option<String> = row.get(1).unwrap();
        if tekst.is_none() {
            total_skipped += 1;
            continue;
        }
        let base_form: String = tekst.clone().unwrap();
        let forms: Vec<String> = vec![base_form.clone()];
        engine.add_word_with_original_id(original_db_id, base_form, word_type.clone(), forms);
        total_imported += 1;
    }

    println!("Total imported: {} words ({} skipped)", total_imported, total_skipped);

    // Save dictionary
    println!("Saving dictionary to disk...");
    println!("NOTE: If stack overflow occurs, run with: RUST_MIN_STACK=33554432");
    let save_start = Instant::now();
    engine.save(output_path)?;
    let save_time = save_start.elapsed();
    println!("Dictionary saved in {:.2} seconds", save_time.as_secs_f64());

    // Final statistics
    let total_time = start_time.elapsed();
    let stats = engine.get_stats();

    println!("\n================================================================================");
    println!("IMPORT COMPLETE");
    println!("================================================================================");
    println!("Total time:   {:.2} seconds ({:.2} minutes)", total_time.as_secs_f64(), total_time.as_secs_f64() / 60.0);
    println!("Words:        {}", stats.get("total_words").unwrap_or(&"0".to_string()));
    println!("Average speed: {:.1} words/sec", total_imported as f64 / total_time.as_secs_f64());
    println!("Dictionary file: {:?}", output_path);

    if let Ok(metadata) = std::fs::metadata(output_path) {
        let size_mb = metadata.len() as f64 / (1024.0 * 1024.0);
        println!("Dictionary size: {:.2} MB", size_mb);
    }

    println!("================================================================================");

    Ok(())
}

fn cmd_odr_import(
    host: &str,
    port: u16,
    database: &str,
    user: &str,
    password: &str,
    force: bool,
    limit: Option<usize>,
    output_path: &PathBuf,
) -> anyhow::Result<()> {
    use mysql::prelude::*;
    use mysql::*;
    use search_engine::text_utils::prepare_variants;
    use std::time::Instant;

    // Check if dictionary exists
    if output_path.exists() && !force {
        println!("✗ Dictionary already exists at {:?}", output_path);
        println!("  Use --force to overwrite");
        return Ok(());
    }

    if output_path.exists() && force {
        println!("⚠ Removing existing dictionary at {:?}", output_path);
        std::fs::remove_file(output_path)?;
    }

    println!("================================================================================");
    println!("ODREDNICA DICTIONARY IMPORT");
    println!("================================================================================");
    println!("Database: {}@{}:{}", database, host, port);
    println!("Output:   {:?}", output_path);
    println!("================================================================================\n");

    // Connect to database
    println!("→ Connecting to database...");
    let url = format!("mysql://{}:{}@{}:{}/{}", user, password, host, port, database);
    let pool = Pool::new(url.as_str())?;
    let mut conn = pool.get_conn()?;
    println!("✓ Connected to database\n");

    // Count entries
    println!("→ Counting entries...");
    let count: i64 = conn.query_first("SELECT COUNT(*) FROM odrednice_odrednica")?.unwrap_or(0);
    let total_entries = if let Some(lim) = limit {
        count.min(lim as i64)
    } else {
        count
    };
    println!("✓ Found {} entries\n", total_entries);

    // Create odrednica engine
    let mut engine = OdrednicaEngine::new();

    println!("→ Importing entries...");
    let start_time = Instant::now();

    let query = if let Some(lim) = limit {
        format!(
            "SELECT id, rec, ijekavski, vrsta, rbr_homonima, sortable_rec FROM odrednice_odrednica LIMIT {}",
            lim
        )
    } else {
        "SELECT id, rec, ijekavski, vrsta, rbr_homonima, sortable_rec FROM odrednice_odrednica".to_string()
    };

    let rows: Vec<Row> = conn.query(query)?;

    let mut imported = 0;
    let mut skipped = 0;

    for row in rows {
        let original_id: i32 = row.get(0).unwrap();
        let rec: Option<String> = row.get(1).unwrap();
        if rec.is_none() {
            skipped += 1;
            continue;
        }
        let rec = rec.unwrap();
        let ijekavski: Option<String> = row.get(2).unwrap();
        let vrsta: i32 = row.get(3).unwrap();
        let rbr_homonima: Option<i32> = row.get(4).unwrap();
        let sortable_rec: Option<String> = row.get(5).unwrap();
        let ociscena_rec = sortable_rec.unwrap_or_else(|| rec.clone());

        // Fetch variants for this entry
        let var_rows: Vec<(Option<String>, Option<String>)> = conn.exec(
            "SELECT tekst, ijekavski FROM odrednice_varijantaodrednice WHERE odrednica_id = ? ORDER BY redni_broj",
            (original_id,),
        )?;

        let varijante = prepare_variants(
            &rec,
            ijekavski.as_deref(),
            &var_rows,
        );

        engine.add_entry(original_id, rec, varijante, vrsta, rbr_homonima, ociscena_rec);
        imported += 1;

        if (imported + skipped) % 1000 == 0 {
            let elapsed = start_time.elapsed().as_secs_f64();
            let rate = (imported + skipped) as f64 / elapsed;
            let eta = (total_entries - imported - skipped) as f64 / rate;
            println!(
                "  Progress: {}/{} ({:.1}%) | Speed: {:.1} entries/sec | ETA: {:.1} sec",
                imported + skipped,
                total_entries,
                100.0 * (imported + skipped) as f64 / total_entries as f64,
                rate,
                eta
            );
        }
    }

    println!("\n✓ Imported {} entries ({} skipped - no rec)", imported, skipped);

    // Save dictionary
    println!("\n→ Saving dictionary to disk...");
    let save_start = Instant::now();
    engine.save(output_path)?;
    let save_time = save_start.elapsed();
    println!("✓ Dictionary saved in {:.2} seconds", save_time.as_secs_f64());

    // Final statistics
    let total_time = start_time.elapsed();
    let stats = engine.get_stats();

    println!("\n================================================================================");
    println!("ODREDNICA IMPORT COMPLETE");
    println!("================================================================================");
    println!("Total time:    {:.2} seconds ({:.2} minutes)", total_time.as_secs_f64(), total_time.as_secs_f64() / 60.0);
    println!("Entries:       {}", stats.get("total_entries").unwrap_or(&"0".to_string()));
    println!("Average speed: {:.1} entries/sec", imported as f64 / total_time.as_secs_f64());
    println!("Dictionary:    {:?}", output_path);

    if let Ok(metadata) = std::fs::metadata(output_path) {
        let size_mb = metadata.len() as f64 / (1024.0 * 1024.0);
        println!("Size:          {:.2} MB", size_mb);
    }

    println!("================================================================================");

    Ok(())
}

fn cmd_odr_stats(dict_path: &PathBuf) -> anyhow::Result<()> {
    if !dict_path.exists() {
        println!("✗ Dictionary file not found: {:?}", dict_path);
        return Ok(());
    }

    let engine = OdrednicaEngine::load(dict_path)?;
    let stats = engine.get_stats();

    println!("\n=== Odrednica Dictionary Statistics ===");
    for (key, value) in stats {
        println!("{}: {}", key, value);
    }

    Ok(())
}

fn cmd_naslov_import(
    host: &str,
    port: u16,
    database: &str,
    user: &str,
    password: &str,
    force: bool,
    output_path: &PathBuf,
) -> anyhow::Result<()> {
    use mysql::prelude::*;
    use mysql::*;
    use search_engine::text_utils::cyr_to_lat;
    use std::time::Instant;

    if output_path.exists() && !force {
        println!("✗ Naslov index already exists at {:?}", output_path);
        println!("  Use --force to overwrite");
        return Ok(());
    }

    if output_path.exists() && force {
        println!("⚠ Removing existing naslov index at {:?}", output_path);
        std::fs::remove_file(output_path)?;
    }

    println!("================================================================================");
    println!("NASLOV (PUBLICATION TITLES) IMPORT");
    println!("================================================================================");
    println!("Database: {}@{}:{}", database, host, port);
    println!("Output:   {:?}", output_path);
    println!("================================================================================\n");

    println!("→ Connecting to database...");
    let url = format!("mysql://{}:{}@{}:{}/{}", user, password, host, port, database);
    let pool = Pool::new(url.as_str())?;
    let mut conn = pool.get_conn()?;
    println!("✓ Connected to database\n");

    println!("→ Counting publications...");
    let count: i64 = conn.query_first("SELECT COUNT(*) FROM publikacije_publikacija")?.unwrap_or(0);
    println!("✓ Found {} publications\n", count);

    let mut engine = NaslovEngine::new();

    println!("→ Importing publication titles...");
    let start_time = Instant::now();

    let rows: Vec<(i32, Option<String>, Option<String>)> = conn.query(
        "SELECT p.id, p.skracenica, pk.naziv \
         FROM publikacije_publikacija p \
         LEFT JOIN publikacije_potkorpus pk ON p.potkorpus_id = pk.id"
    )?;

    let mut imported = 0;

    for (pub_id, skracenica, potkorpus) in rows {
        let skracenica = skracenica.unwrap_or_default();
        let potkorpus = potkorpus.unwrap_or_default();

        // Build opis the same way Django does: authors + title + publisher + year etc.
        // We query the authors separately
        let authors: Vec<(String, String)> = conn.exec(
            "SELECT prezime, ime FROM publikacije_autor WHERE publikacija_id = ? ORDER BY redni_broj",
            (pub_id,),
        )?;

        let naslov: Option<String> = conn.exec_first(
            "SELECT naslov FROM publikacije_publikacija WHERE id = ?",
            (pub_id,),
        )?;

        let autor_str = if !authors.is_empty() {
            authors.iter()
                .map(|(prezime, ime)| format!("{}, {}", prezime, ime))
                .collect::<Vec<_>>()
                .join("; ")
        } else {
            String::new()
        };

        let naslov_str = naslov.unwrap_or_default();
        let opis = if autor_str.is_empty() {
            naslov_str.clone()
        } else {
            format!("{}: {}", autor_str, naslov_str)
        };

        // Add both Cyrillic and Latin versions for searchability
        let opis_lat = cyr_to_lat(&opis);
        let opis_combined = format!("{} {}", opis, opis_lat);

        engine.add_entry(pub_id, skracenica, opis_combined, potkorpus);
        imported += 1;

        if imported % 1000 == 0 {
            let elapsed = start_time.elapsed().as_secs_f64();
            let rate = imported as f64 / elapsed;
            println!(
                "  Progress: {}/{} ({:.1}%) | Speed: {:.1} pubs/sec",
                imported, count,
                100.0 * imported as f64 / count as f64,
                rate
            );
        }
    }

    println!("\n✓ Imported {} publication titles", imported);

    println!("\n→ Saving naslov index to disk...");
    let save_start = Instant::now();
    engine.save(output_path)?;
    let save_time = save_start.elapsed();
    println!("✓ Index saved in {:.2} seconds", save_time.as_secs_f64());

    let total_time = start_time.elapsed();
    let stats = engine.get_stats();

    println!("\n================================================================================");
    println!("NASLOV IMPORT COMPLETE");
    println!("================================================================================");
    println!("Total time:    {:.2} seconds", total_time.as_secs_f64());
    println!("Entries:       {}", stats.get("total_entries").unwrap_or(&"0".to_string()));
    println!("Average speed: {:.1} pubs/sec", imported as f64 / total_time.as_secs_f64());
    println!("Index file:    {:?}", output_path);

    if let Ok(metadata) = std::fs::metadata(output_path) {
        let size_mb = metadata.len() as f64 / (1024.0 * 1024.0);
        println!("Index size:    {:.2} MB", size_mb);
    }

    println!("================================================================================");

    Ok(())
}

fn cmd_naslov_stats(dict_path: &PathBuf) -> anyhow::Result<()> {
    if !dict_path.exists() {
        println!("✗ Naslov index file not found: {:?}", dict_path);
        return Ok(());
    }

    let engine = NaslovEngine::load(dict_path)?;
    let stats = engine.get_stats();

    println!("\n=== Naslov Index Statistics ===");
    for (key, value) in stats {
        println!("{}: {}", key, value);
    }

    Ok(())
}
