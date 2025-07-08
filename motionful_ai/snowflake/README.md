# 🎨 MotionfulAI SVG Asset Management System

A complete AI-powered SVG asset management system built with Snowflake, featuring web scraping, vector embeddings, and semantic search capabilities.

## 🚀 **System Overview**

This system creates a comprehensive SVG asset pipeline that:
- **Scrapes** SVG assets from sources like SVGRepo and unDraw
- **Stores** structured and unstructured data in Snowflake
- **Generates** vector embeddings for semantic search
- **Provides** a Streamlit dashboard for visualization and search
- **Enables** AI-powered asset discovery for Motion Canvas generation

## 🛠️ **Prerequisites**

### 1. **Snowflake Account Setup**
- Active Snowflake account with ACCOUNTADMIN role
- Warehouse: `COMPUTE_WH`
- Working credentials

### 2. **Python Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Update Configuration**
Edit `config/snowflake_config.py` and replace `'XXXXXXXXXXXXXXXXXX'` with your actual Snowflake password.

## 📁 **Project Structure**

```
motionful_ai/snowflake/
├── config/
│   └── snowflake_config.py      # Database configuration
├── ingestion/
│   ├── svg_scraper.py           # Web scraping logic
│   └── embedding_generator.py   # Vector embeddings
├── sql/
│   └── schema_setup.sql         # Database schema
├── streamlit/
│   └── simple_app.py           # Dashboard application
├── run_svg_pipeline.py          # Main pipeline runner
├── test_connection.py           # Connection tester
└── create_database.py           # Database setup
```

## 🔧 **Setup Instructions**

### Step 1: Test Connection
```bash
cd motionful_ai/snowflake
python test_connection.py
```
Expected output: `✅ Connection successful! Snowflake version: 9.18.0`

### Step 2: Create Database Schema
```bash
python create_database.py
```
This creates:
- Database: `MOTIONFUL_AI`
- Schema: `SVG_ASSETS`
- Tables: `SVG_ASSETS`, `SVG_CONTENT`, `SVG_EMBEDDINGS`

### Step 3: Run the Complete Pipeline
```bash
python run_svg_pipeline.py
```

This will:
1. 🔧 Set up database schema
2. 🔍 Scrape SVGs from multiple categories
3. 💾 Store assets in Snowflake
4. 🧠 Generate vector embeddings
5. 📊 Display statistics
6. 🔍 Test search functionality

### Step 4: Launch Dashboard
```bash
streamlit run streamlit/simple_app.py
```

## 🎯 **Key Features**

### 📊 **Dashboard**
- Real-time asset statistics
- Category distribution charts
- Recent asset listings
- System health monitoring

### 🔍 **Semantic Search**
- AI-powered similarity search
- Vector-based asset discovery
- Relevance scoring
- Fast query response

### ⚙️ **Admin Panel**
- Database operations
- Raw SQL query interface
- System information
- Cache management

## 🗄️ **Database Schema**

### SVG_ASSETS Table
- **ASSET_ID**: Unique identifier
- **TITLE**: Asset title
- **DESCRIPTION**: Asset description
- **CATEGORY**: Asset category (icons, business, etc.)
- **TAGS**: Array of tags
- **COLOR_PALETTE**: Array of colors
- **SOURCE_URL**: Original source URL

### SVG_CONTENT Table
- **ASSET_ID**: Links to SVG_ASSETS
- **SVG_DATA**: JSON containing SVG content
- **SVG_TEXT**: Text representation for search

### SVG_EMBEDDINGS Table
- **ASSET_ID**: Links to SVG_ASSETS
- **EMBEDDING_VECTOR**: 384-dimensional vector
- **EMBEDDING_MODEL**: Model used for embedding

## 🔍 **Search Functionality**

The system uses HuggingFace Sentence Transformers to generate 384-dimensional embeddings for:
- Asset titles and descriptions
- Tag combinations
- SVG metadata

Search queries are converted to embeddings and compared using cosine similarity.

## 📈 **Performance Metrics**

- **Scraping Speed**: ~5-10 assets per category per minute
- **Embedding Generation**: ~100 assets per minute
- **Search Response**: <1 second for datasets up to 1000 assets
- **Storage Efficiency**: Structured + unstructured data coexistence

## 🏆 **Snowflake Prize Alignment**

This project demonstrates:
- ✅ **Structured Data**: Asset metadata, categories, statistics
- ✅ **Unstructured Data**: SVG content, embeddings, JSON metadata
- ✅ **Data Transformation**: Web scraping → structured storage
- ✅ **AI Integration**: Vector embeddings, semantic search
- ✅ **Open Source Tools**: Streamlit dashboard, HuggingFace models
- ✅ **Scalable Architecture**: Async processing, modular design

## 🚨 **Troubleshooting**

### Connection Issues
```bash
# Test connection
python test_connection.py

# Check credentials in config/snowflake_config.py
# Ensure warehouse COMPUTE_WH exists
```

### Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Database Errors
```bash
# Recreate database
python create_database.py

# Check permissions
# Ensure ACCOUNTADMIN role is active
```

## 💡 **Usage Examples**

### Basic Search
```python
# Search for business icons
results = pipeline.search_assets("business icon", limit=5)
for result in results:
    print(f"{result['title']} - {result['similarity']:.3f}")
```

### Data Analytics
```python
# Get statistics
stats = pipeline.get_statistics()
print(f"Total assets: {stats['total_assets']}")
print(f"Categories: {stats['categories']}")
```

### Asset Storage
```python
# Store new asset
asset_data = {
    'asset_id': 'unique_id',
    'title': 'Business Icon',
    'description': 'Professional business icon',
    'category': 'business',
    'svg_content': '<svg>...</svg>',
    'source_url': 'https://example.com'
}
pipeline.store_assets([asset_data])
```

## 🔮 **Future Enhancements**

- **Vultr Integration**: Cloud deployment
- **Motion Canvas Integration**: Direct code generation
- **Real-time Updates**: Live asset monitoring
- **Advanced Analytics**: Usage tracking, trends
- **Multi-modal Search**: Image-based search
- **API Endpoints**: RESTful asset API

## 🏅 **Hackathon Success Metrics**

- [x] **Working Snowflake Integration**
- [x] **AI-Powered Search**
- [x] **Streamlit Dashboard**
- [x] **Data Pipeline**
- [x] **Vector Embeddings**
- [x] **Structured + Unstructured Data**
- [x] **Open Source Tools**
- [x] **Scalable Architecture**

---

## 🎯 **Quick Start Command**

```bash
# Run everything in sequence
python test_connection.py && \
python create_database.py && \
python run_svg_pipeline.py && \
streamlit run streamlit/simple_app.py
```

**�� Happy Hacking!** 