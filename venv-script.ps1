# Define paths
$project_dir = "Le/chemin/du/projet"
$requirements_file = "$project_dir\requirements.txt"
$venv_dir = "$project_dir\venv"

# Update requirements.txt

# Activate virtual environment if exists
$venv_activate = "$venv_dir\Scripts\Activate.ps1"
if (Test-Path $venv_activate) {
    . $venv_activate
} else {
    Write-Host "Virtual environment not found. Creating..."
    # Create virtual environment
    python -m venv $venv_dir
    . $venv_activate
}

# Install pip-tools to manage requirements
pip install pip-tools

# Generate requirements file
pip-compile --output-file=$requirements_file $project_dir\requirements.in

# Install the requirements
pip install -r $requirements_file