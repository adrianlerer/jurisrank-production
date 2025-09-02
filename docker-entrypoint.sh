#!/bin/bash
# JurisRank Docker Entrypoint Script
# Handles initialization and graceful startup

set -e

# Function to wait for dependencies
wait_for_dependencies() {
    echo "🔧 Checking dependencies..."
    python3 -c "import flask, requests, sqlite3; print('✅ All dependencies available')"
}

# Function to initialize database
initialize_database() {
    echo "🗄️ Initializing database..."
    if [ ! -f "/app/bibliography.db" ]; then
        python3 -c "
import sqlite3
conn = sqlite3.connect('/app/bibliography.db')
conn.execute('''CREATE TABLE IF NOT EXISTS bibliography_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    year INTEGER,
    url TEXT,
    doi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
conn.close()
print('✅ Database initialized successfully')
"
    else
        echo "✅ Database already exists"
    fi
}

# Function to validate configuration
validate_config() {
    echo "⚙️ Validating configuration..."
    
    # Check required files
    required_files=("bibliography_api.py" "requirements.txt")
    for file in "${required_files[@]}"; do
        if [ ! -f "/app/$file" ]; then
            echo "❌ Required file missing: $file"
            exit 1
        fi
    done
    
    echo "✅ Configuration valid"
}

# Function to start appropriate service
start_service() {
    if [ "${DEV_MODE:-0}" = "1" ]; then
        echo "🚀 Starting JurisRank in DEVELOPMENT mode..."
        exec python3 mock_api_server.py
    else
        echo "🚀 Starting JurisRank in PRODUCTION mode..."
        exec python3 bibliography_api.py
    fi
}

# Main execution
main() {
    echo "🏛️ JurisRank AI: Constitutional Analysis API"
    echo "🐳 Container Version: 0.3.0"
    echo "📅 $(date)"
    echo "----------------------------------------"
    
    # Ensure proper permissions
    chown -R jurisrank:jurisrank /app/logs /app/data 2>/dev/null || true
    
    # Run initialization steps
    wait_for_dependencies
    validate_config
    initialize_database
    
    # Start the appropriate service
    start_service
}

# Execute main function
main "$@"