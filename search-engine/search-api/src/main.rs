use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use search_engine::{DocumentMetadata, SearchEngine, MorphologyEngine, OdrednicaEngine, OdrednicaEntry, NaslovEngine, NaslovEntry, WordEntry};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use tower_http::cors::{Any, CorsLayer};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

type SharedEngine = Arc<RwLock<SearchEngine>>;
type SharedMorphology = Arc<RwLock<MorphologyEngine>>;
type SharedOdrednica = Arc<RwLock<OdrednicaEngine>>;
type SharedNaslov = Arc<RwLock<NaslovEngine>>;

#[derive(Clone)]
struct AppState {
    engine: SharedEngine,
    morphology: SharedMorphology,
    odrednica: SharedOdrednica,
    naslov: SharedNaslov,
}

#[derive(Debug, Serialize, Deserialize)]
struct SearchRequest {
    phrase: String,
    #[serde(default = "default_fragment_size")]
    fragment_size: usize,
    #[serde(default = "default_mode")]
    mode: String,
}

fn default_fragment_size() -> usize {
    20
}

fn default_mode() -> String {
    "word".to_string()
}

#[derive(Debug, Serialize)]
struct SearchResponse {
    query: String,
    results: Vec<SearchResultResponse>,
    total_matches: usize,
    execution_time_ms: f64,
}

#[derive(Debug, Serialize)]
struct SearchResultResponse {
    doc_id: i32,
    metadata: DocumentMetadata,
    fragments: Vec<String>,
}

#[derive(Debug, Serialize)]
struct StatsResponse {
    stats: HashMap<String, String>,
}

#[derive(Debug, Serialize)]
struct HealthResponse {
    status: String,
    index_loaded: bool,
}

#[derive(Debug, Deserialize)]
struct PrefixQuery {
    #[serde(default = "default_limit")]
    limit: usize,
}

fn default_limit() -> usize {
    10
}

#[derive(Debug, Serialize, Deserialize)]
struct MultiWordSearchRequest {
    words: Vec<String>,
    #[serde(default = "default_fragment_size")]
    fragment_size: usize,
    #[serde(default = "default_mode")]
    mode: String,
}

#[derive(Debug, Serialize)]
struct MultiWordSearchResponse {
    words: Vec<String>,
    results: Vec<SearchResultResponse>,
    total_matches: usize,
    execution_time_ms: f64,
}

#[derive(Debug, Serialize)]
struct MorphologyWordResponse {
    id: i32,
    original_id: Option<i32>,
    base_form: String,
    word_type: String,
    forms: Vec<String>,
}

impl From<WordEntry> for MorphologyWordResponse {
    fn from(entry: WordEntry) -> Self {
        Self {
            id: entry.id,
            original_id: entry.original_id,
            base_form: entry.base_form,
            word_type: entry.word_type.to_string(),
            forms: entry.forms,
        }
    }
}

#[derive(Debug, Serialize)]
struct MorphologySearchResponse {
    form: String,
    results: Vec<MorphologyWordResponse>,
    total_matches: usize,
}

#[derive(Debug, Serialize)]
struct MorphologyPrefixResponse {
    prefix: String,
    results: Vec<MorphologyWordResponse>,
    total_matches: usize,
}

#[derive(Debug, Serialize)]
struct MorphologySuffixResponse {
    suffix: String,
    results: Vec<MorphologyWordResponse>,
    total_matches: usize,
}

#[derive(Debug, Serialize)]
struct OdrednicaResponse {
    id: i32,
    original_id: i32,
    rec: String,
    vrsta: i32,
    rbr_homonima: Option<i32>,
    ociscena_rec: String,
}

impl From<OdrednicaEntry> for OdrednicaResponse {
    fn from(entry: OdrednicaEntry) -> Self {
        Self {
            id: entry.id,
            original_id: entry.original_id,
            rec: entry.rec,
            vrsta: entry.vrsta,
            rbr_homonima: entry.rbr_homonima,
            ociscena_rec: entry.ociscena_rec,
        }
    }
}

#[derive(Debug, Serialize)]
struct OdrednicaPrefixResponse {
    prefix: String,
    results: Vec<OdrednicaResponse>,
    total_matches: usize,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "search_api=info,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let index_path = std::env::var("INDEX_PATH").unwrap_or_else(|_| "search_index/search_index.bin".to_string());

    let engine = if std::path::Path::new(&index_path).exists() {
        tracing::info!("Loading index from {}", index_path);
        match SearchEngine::load(&index_path) {
            Ok(eng) => {
                tracing::info!("✓ Index loaded successfully");
                eng
            }
            Err(e) => {
                tracing::warn!("Failed to load index: {}. Starting with empty engine.", e);
                SearchEngine::new()
            }
        }
    } else {
        tracing::info!("No index found. Starting with empty engine.");
        SearchEngine::new()
    };

    // Load morphology dictionary
    let morphology_path = std::env::var("MORPHOLOGY_PATH")
        .unwrap_or_else(|_| "search_index/morphology.bin".to_string());

    let morphology = if std::path::Path::new(&morphology_path).exists() {
        tracing::info!("Loading morphology dictionary from {}", morphology_path);
        match MorphologyEngine::load(&morphology_path) {
            Ok(morph) => {
                tracing::info!("✓ Morphology dictionary loaded successfully");
                morph
            }
            Err(e) => {
                tracing::warn!("Failed to load morphology dictionary: {}. Starting empty.", e);
                MorphologyEngine::new()
            }
        }
    } else {
        tracing::info!("No morphology dictionary found. Starting with empty dictionary.");
        MorphologyEngine::new()
    };

    // Load odrednica dictionary
    let odrednica_path = std::env::var("ODREDNICA_PATH")
        .unwrap_or_else(|_| "search_index/odrednica.bin".to_string());

    let odrednica = if std::path::Path::new(&odrednica_path).exists() {
        tracing::info!("Loading odrednica dictionary from {}", odrednica_path);
        match OdrednicaEngine::load(&odrednica_path) {
            Ok(odr) => {
                tracing::info!("✓ Odrednica dictionary loaded successfully");
                odr
            }
            Err(e) => {
                tracing::warn!("Failed to load odrednica dictionary: {}. Starting empty.", e);
                OdrednicaEngine::new()
            }
        }
    } else {
        tracing::info!("No odrednica dictionary found. Starting with empty dictionary.");
        OdrednicaEngine::new()
    };

    // Load naslov (publication titles) index
    let naslov_path = std::env::var("NASLOV_PATH")
        .unwrap_or_else(|_| "search_index/naslov.bin".to_string());

    let naslov = if std::path::Path::new(&naslov_path).exists() {
        tracing::info!("Loading naslov index from {}", naslov_path);
        match NaslovEngine::load(&naslov_path) {
            Ok(nas) => {
                tracing::info!("✓ Naslov index loaded successfully");
                nas
            }
            Err(e) => {
                tracing::warn!("Failed to load naslov index: {}. Starting empty.", e);
                NaslovEngine::new()
            }
        }
    } else {
        tracing::info!("No naslov index found. Starting with empty index.");
        NaslovEngine::new()
    };

    let state = AppState {
        engine: Arc::new(RwLock::new(engine)),
        morphology: Arc::new(RwLock::new(morphology)),
        odrednica: Arc::new(RwLock::new(odrednica)),
        naslov: Arc::new(RwLock::new(naslov)),
    };

    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/health/detailed", get(health_detailed))
        .route("/stats", get(stats))
        .route("/search", post(search))
        .route("/search/multi", post(multi_word_search))
        .route("/prefix/:prefix", get(prefix_search))
        .route("/suffix/:suffix", get(suffix_search))
        .route("/document/:id", get(get_document))
        .route("/morphology/form/:form", get(morphology_search_form))
        .route("/morphology/prefix/:prefix", get(morphology_search_prefix))
        .route("/morphology/suffix/:suffix", get(morphology_search_suffix))
        .route("/morphology/stats", get(morphology_stats))
        .route("/odrednica/prefix/:prefix", get(odrednica_search_prefix))
        .route("/odrednica/stats", get(odrednica_stats))
        .route("/naslov/stats", get(naslov_stats))
        .route("/naslov/prefix/:prefix", get(naslov_search_prefix))
        .route("/naslov/:id", get(naslov_get_by_id))
        .layer(CorsLayer::new().allow_origin(Any).allow_methods(Any).allow_headers(Any))
        .with_state(state);

    let addr = std::env::var("HOST")
        .unwrap_or_else(|_| "0.0.0.0".to_string())
        + ":"
        + &std::env::var("PORT").unwrap_or_else(|_| "9090".to_string());

    tracing::info!("Starting server on {}", addr);

    let listener = tokio::net::TcpListener::bind(&addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}

async fn root() -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok".to_string(),
        index_loaded: true,
    })
}

async fn health(State(state): State<AppState>) -> Json<HealthResponse> {
    let engine = state.engine.read().unwrap();
    let loaded = !engine.get_stats().is_empty();

    Json(HealthResponse {
        status: "ok".to_string(),
        index_loaded: loaded,
    })
}

async fn health_detailed(State(state): State<AppState>) -> Json<HashMap<String, serde_json::Value>> {
    let engine = state.engine.read().unwrap();
    let stats = engine.get_stats();

    let mut response = HashMap::new();
    response.insert("status".to_string(), serde_json::json!("healthy"));
    response.insert("stats".to_string(), serde_json::json!(stats));

    Json(response)
}

async fn stats(State(state): State<AppState>) -> Json<StatsResponse> {
    let engine = state.engine.read().unwrap();
    let stats = engine.get_stats();

    Json(StatsResponse { stats })
}

async fn search(
    State(state): State<AppState>,
    Json(req): Json<SearchRequest>,
) -> Result<Json<SearchResponse>, (StatusCode, String)> {
    let start = std::time::Instant::now();

    let engine = state.engine.read().unwrap();

    let results = engine
        .search_phrase(&req.phrase, req.fragment_size, &req.mode)
        .map_err(|e| (StatusCode::BAD_REQUEST, e.to_string()))?;

    let execution_time_ms = start.elapsed().as_secs_f64() * 1000.0;

    let response_results: Vec<SearchResultResponse> = results
        .into_iter()
        .map(|r| SearchResultResponse {
            doc_id: r.doc_id,
            metadata: r.metadata,
            fragments: r.fragments,
        })
        .collect();

    Ok(Json(SearchResponse {
        query: req.phrase,
        total_matches: response_results.len(),
        results: response_results,
        execution_time_ms,
    }))
}

async fn prefix_search(
    State(state): State<AppState>,
    Path(prefix): Path<String>,
    Query(params): Query<PrefixQuery>,
) -> Json<HashMap<String, serde_json::Value>> {
    let engine = state.engine.read().unwrap();
    let words = engine.prefix_search(&prefix);

    let limited_words: Vec<String> = words.into_iter().take(params.limit).collect();
    let total = limited_words.len();

    let mut response = HashMap::new();
    response.insert("prefix".to_string(), serde_json::json!(prefix));
    response.insert("matches".to_string(), serde_json::json!(limited_words));
    response.insert("total_matches".to_string(), serde_json::json!(total));

    Json(response)
}

async fn suffix_search(
    State(state): State<AppState>,
    Path(suffix): Path<String>,
    Query(params): Query<PrefixQuery>,
) -> Json<HashMap<String, serde_json::Value>> {
    let engine = state.engine.read().unwrap();
    let words = engine.suffix_word_search(&suffix);

    let limited_words: Vec<String> = words.into_iter().take(params.limit).collect();
    let total = limited_words.len();

    let mut response = HashMap::new();
    response.insert("suffix".to_string(), serde_json::json!(suffix));
    response.insert("matches".to_string(), serde_json::json!(limited_words));
    response.insert("total_matches".to_string(), serde_json::json!(total));

    Json(response)
}

async fn get_document(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<HashMap<String, serde_json::Value>>, (StatusCode, String)> {
    let engine = state.engine.read().unwrap();

    match engine.get_document(id) {
        Some(text) => {
            let mut response = HashMap::new();
            response.insert("doc_id".to_string(), serde_json::json!(id));
            response.insert("text".to_string(), serde_json::json!(text));
            Ok(Json(response))
        }
        None => Err((
            StatusCode::NOT_FOUND,
            format!("Document {} not found", id),
        )),
    }
}

async fn multi_word_search(
    State(state): State<AppState>,
    Json(req): Json<MultiWordSearchRequest>,
) -> Result<Json<MultiWordSearchResponse>, (StatusCode, String)> {
    let start = std::time::Instant::now();

    if req.words.is_empty() {
        return Err((StatusCode::BAD_REQUEST, "No words provided".to_string()));
    }

    let engine = state.engine.read().unwrap();

    // Use a HashMap to collect unique documents and their fragments
    let mut doc_map: HashMap<i32, (DocumentMetadata, Vec<String>)> = HashMap::new();

    // Search for each word separately
    for word in &req.words {
        let word_results = engine
            .search_phrase(word, req.fragment_size, &req.mode)
            .map_err(|e| (StatusCode::BAD_REQUEST, e.to_string()))?;

        // Merge results into the doc_map
        for result in word_results {
            doc_map
                .entry(result.doc_id)
                .and_modify(|(_, fragments)| {
                    // Add new fragments, avoiding exact duplicates
                    for fragment in &result.fragments {
                        if !fragments.contains(fragment) {
                            fragments.push(fragment.clone());
                        }
                    }
                })
                .or_insert((result.metadata.clone(), result.fragments));
        }
    }

    // Convert HashMap back to Vec of SearchResultResponse
    let mut results: Vec<SearchResultResponse> = doc_map
        .into_iter()
        .map(|(doc_id, (metadata, fragments))| SearchResultResponse {
            doc_id,
            metadata,
            fragments,
        })
        .collect();

    // Sort by doc_id for consistent ordering
    results.sort_by_key(|r| r.doc_id);

    let execution_time_ms = start.elapsed().as_secs_f64() * 1000.0;

    Ok(Json(MultiWordSearchResponse {
        words: req.words,
        total_matches: results.len(),
        results,
        execution_time_ms,
    }))
}

async fn morphology_search_form(
    State(state): State<AppState>,
    Path(form): Path<String>,
) -> Json<MorphologySearchResponse> {
    let morphology = state.morphology.read().unwrap();
    let words = morphology.search_by_form(&form);

    let results: Vec<MorphologyWordResponse> = words.into_iter().map(|w| w.into()).collect();

    Json(MorphologySearchResponse {
        form,
        total_matches: results.len(),
        results,
    })
}

async fn morphology_search_prefix(
    State(state): State<AppState>,
    Path(prefix): Path<String>,
    Query(params): Query<PrefixQuery>,
) -> Json<MorphologyPrefixResponse> {
    let morphology = state.morphology.read().unwrap();
    let words = morphology.search_by_prefix(&prefix);

    let limited_words: Vec<WordEntry> = words.into_iter().take(params.limit).collect();
    let results: Vec<MorphologyWordResponse> = limited_words.into_iter().map(|w| w.into()).collect();

    Json(MorphologyPrefixResponse {
        prefix,
        total_matches: results.len(),
        results,
    })
}

async fn morphology_search_suffix(
    State(state): State<AppState>,
    Path(suffix): Path<String>,
    Query(params): Query<PrefixQuery>,
) -> Json<MorphologySuffixResponse> {
    let morphology = state.morphology.read().unwrap();
    let words = morphology.search_by_suffix(&suffix);

    let limited_words: Vec<WordEntry> = words.into_iter().take(params.limit).collect();
    let results: Vec<MorphologyWordResponse> = limited_words.into_iter().map(|w| w.into()).collect();

    Json(MorphologySuffixResponse {
        suffix,
        total_matches: results.len(),
        results,
    })
}

async fn morphology_stats(State(state): State<AppState>) -> Json<HashMap<String, String>> {
    let morphology = state.morphology.read().unwrap();
    let stats = morphology.get_stats();

    Json(stats)
}

async fn odrednica_search_prefix(
    State(state): State<AppState>,
    Path(prefix): Path<String>,
    Query(params): Query<PrefixQuery>,
) -> Json<OdrednicaPrefixResponse> {
    let odrednica = state.odrednica.read().unwrap();
    let entries = odrednica.search_by_prefix(&prefix);

    let limited: Vec<OdrednicaEntry> = entries.into_iter().take(params.limit).collect();
    let results: Vec<OdrednicaResponse> = limited.into_iter().map(|e| e.into()).collect();

    Json(OdrednicaPrefixResponse {
        prefix,
        total_matches: results.len(),
        results,
    })
}

async fn odrednica_stats(State(state): State<AppState>) -> Json<HashMap<String, String>> {
    let odrednica = state.odrednica.read().unwrap();
    let stats = odrednica.get_stats();

    Json(stats)
}

#[derive(Debug, Serialize)]
struct NaslovResponse {
    id: i32,
    original_id: i32,
    skracenica: String,
    opis: String,
    potkorpus: String,
}

impl From<NaslovEntry> for NaslovResponse {
    fn from(entry: NaslovEntry) -> Self {
        Self {
            id: entry.id,
            original_id: entry.original_id,
            skracenica: entry.skracenica,
            opis: entry.opis,
            potkorpus: entry.potkorpus,
        }
    }
}

#[derive(Debug, Serialize)]
struct NaslovPrefixResponse {
    prefix: String,
    results: Vec<NaslovResponse>,
    total_matches: usize,
}

async fn naslov_search_prefix(
    State(state): State<AppState>,
    Path(prefix): Path<String>,
    Query(params): Query<PrefixQuery>,
) -> Json<NaslovPrefixResponse> {
    let naslov = state.naslov.read().unwrap();
    let entries = naslov.search_by_prefix(&prefix);

    let limited: Vec<NaslovEntry> = entries.into_iter().take(params.limit).collect();
    let results: Vec<NaslovResponse> = limited.into_iter().map(|e| e.into()).collect();

    Json(NaslovPrefixResponse {
        prefix,
        total_matches: results.len(),
        results,
    })
}

async fn naslov_get_by_id(
    State(state): State<AppState>,
    Path(id): Path<i32>,
) -> Result<Json<NaslovResponse>, (StatusCode, String)> {
    let naslov = state.naslov.read().unwrap();

    match naslov.get_entry_by_original_id(id) {
        Some(entry) => Ok(Json(entry.clone().into())),
        None => Err((
            StatusCode::NOT_FOUND,
            format!("Naslov with ID {} not found", id),
        )),
    }
}

async fn naslov_stats(State(state): State<AppState>) -> Json<HashMap<String, String>> {
    let naslov = state.naslov.read().unwrap();
    let stats = naslov.get_stats();

    Json(stats)
}
