# Build and deploy admin panel script
Write-Host "Starting admin panel build and deploy process..."

# Install dependencies
Write-Host "Installing dependencies..."
npm install

# Build the admin panel
Write-Host "Building admin panel..."
npm run build

# Create admin static directory in backend if it doesn't exist
$backendAdminStaticPath = "..\backend\static\admin"
if (-not (Test-Path $backendAdminStaticPath)) {
    Write-Host "Creating admin static directory in backend..."
    New-Item -ItemType Directory -Path $backendAdminStaticPath -Force
}

# Copy built files to backend admin static directory
Write-Host "Copying built files to backend admin directory..."
Copy-Item -Path "build\*" -Destination $backendAdminStaticPath -Recurse -Force

Write-Host "Admin panel build and deploy completed successfully!" 