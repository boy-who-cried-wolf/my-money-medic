# Build and deploy frontend script
Write-Host "Starting frontend build and deploy process..."

# Install dependencies
Write-Host "Installing dependencies..."
npm install

# Build the frontend
Write-Host "Building frontend..."
npm run build

# Create static directory in backend if it doesn't exist
$backendStaticPath = "..\backend\static"
if (-not (Test-Path $backendStaticPath)) {
    Write-Host "Creating static directory in backend..."
    New-Item -ItemType Directory -Path $backendStaticPath -Force
}

# Copy built files to backend static directory
Write-Host "Copying built files to backend..."
Copy-Item -Path "build\*" -Destination $backendStaticPath -Recurse -Force

Write-Host "Frontend build and deploy completed successfully!" 