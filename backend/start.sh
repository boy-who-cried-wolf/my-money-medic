# Railway startup script

# Set default port if not provided
export PORT=${PORT:-8000}

echo "Starting server on port $PORT"
python server.py 