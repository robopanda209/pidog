#!/bin/bash

# PiDog Dual Installation Script
# This script installs both Official and Custom (robopanda209) PiDog versions
# Author: Setup for dual PiDog development environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_DIR="/home/steve/Development"
OFFICIAL_DIR="$BASE_DIR/Official"
CUSTOM_DIR="$BASE_DIR/Custom"
OFFICIAL_REPO="https://github.com/sunfounder/pidog.git"
CUSTOM_REPO="https://github.com/robopanda209/pidog.git"
ROBOT_HAT_REPO="https://github.com/sunfounder/robot-hat.git"
VILIB_REPO="https://github.com/sunfounder/vilib.git"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}================================================${NC}\n"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system dependencies
install_system_deps() {
    print_header "Installing System Dependencies"
    
    print_status "Updating package list..."
    sudo apt update
    
    print_status "Installing required packages..."
    sudo apt install -y git python3-pip python3-setuptools python3-smbus python3-venv
    
    print_success "System dependencies installed"
}

# Function to create directory structure
create_directories() {
    print_header "Creating Directory Structure"
    
    print_status "Creating base directory: $BASE_DIR"
    mkdir -p "$BASE_DIR"
    
    print_status "Creating Official directory: $OFFICIAL_DIR"
    mkdir -p "$OFFICIAL_DIR"
    
    print_status "Creating Custom directory: $CUSTOM_DIR"
    mkdir -p "$CUSTOM_DIR"
    
    print_success "Directory structure created"
}

# Function to clone repository with error handling
clone_repo() {
    local repo_url=$1
    local target_dir=$2
    local repo_name=$3
    
    if [ -d "$target_dir" ]; then
        print_warning "$repo_name already exists at $target_dir"
        read -p "Do you want to remove and re-clone? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$target_dir"
        else
            print_status "Skipping $repo_name clone"
            return 0
        fi
    fi
    
    print_status "Cloning $repo_name..."
    git clone "$repo_url" "$target_dir"
    print_success "$repo_name cloned successfully"
}

# Function to setup virtual environment and install packages
setup_environment() {
    local env_dir=$1
    local env_name=$2
    local pidog_dir=$3
    local deps_base_dir=$4
    
    print_header "Setting up $env_name Environment"
    
    # Create virtual environment
    print_status "Creating virtual environment at $env_dir"
    python3 -m venv "$env_dir"
    
    # Activate environment
    source "$env_dir/bin/activate"
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install basic dependencies first
    print_status "Installing Python dependencies..."
    pip install setuptools wheel
    
    # Install robot-hat FIRST (before PiDog, since PiDog depends on it)
    print_status "Installing robot-hat library..."
    cd "$deps_base_dir"
    if [ ! -d "robot-hat" ]; then
        git clone "$ROBOT_HAT_REPO"
    fi
    cd robot-hat
    pip install -e .
    
    # Install vilib
    print_status "Installing vilib library..."
    cd "$deps_base_dir"
    if [ ! -d "vilib" ]; then
        git clone -b picamera2 "$VILIB_REPO" --depth 1
    fi
    cd vilib
    python3 install.py
    
    # Now install PiDog library (after dependencies are installed)
    print_status "Installing PiDog library in development mode..."
    cd "$pidog_dir"
    pip install -e .
    
    # Deactivate environment
    deactivate
    
    print_success "$env_name environment setup complete"
}

# Function to create activation scripts
create_activation_scripts() {
    print_header "Creating Activation Scripts"
    
    # Official activation script
    cat > "$OFFICIAL_DIR/activate_official.sh" << EOF
#!/bin/bash
source "$OFFICIAL_DIR/pidog/venv_official/bin/activate"
echo -e "${GREEN}🤖 Official PiDog environment activated${NC}"
echo -e "${BLUE}📁 Working directory: $OFFICIAL_DIR/pidog${NC}"
cd "$OFFICIAL_DIR/pidog"
EOF
    
    # Custom activation script
    cat > "$CUSTOM_DIR/activate_custom.sh" << EOF
#!/bin/bash
source "$CUSTOM_DIR/pidog/venv_custom/bin/activate"
echo -e "${GREEN}🔧 Custom PiDog environment activated${NC}"
echo -e "${BLUE}📁 Working directory: $CUSTOM_DIR/pidog${NC}"
cd "$CUSTOM_DIR/pidog"
EOF
    
    # Make scripts executable
    chmod +x "$OFFICIAL_DIR/activate_official.sh"
    chmod +x "$CUSTOM_DIR/activate_custom.sh"
    
    print_success "Activation scripts created"
}

# Function to add aliases to bashrc
add_aliases() {
    print_header "Adding Convenience Aliases"
    
    # Check if aliases already exist
    if grep -q "pidog-official" ~/.bashrc; then
        print_warning "PiDog aliases already exist in ~/.bashrc"
        return 0
    fi
    
    print_status "Adding aliases to ~/.bashrc"
    cat >> ~/.bashrc << EOF

# PiDog Environment Aliases
alias pidog-official="source $OFFICIAL_DIR/activate_official.sh"
alias pidog-custom="source $CUSTOM_DIR/activate_custom.sh"
alias pidog-help="echo -e 'PiDog Commands:\n  pidog-official  - Activate official SunFounder version\n  pidog-custom    - Activate custom robopanda209 version\n  deactivate      - Exit current environment'"
EOF
    
    print_success "Aliases added to ~/.bashrc"
    print_status "Run 'source ~/.bashrc' or restart terminal to use aliases"
}

# Function to test installations
test_installations() {
    print_header "Testing Installations"
    
    # Test Official version
    print_status "Testing Official PiDog installation..."
    source "$OFFICIAL_DIR/pidog/venv_official/bin/activate"
    if python3 -c "from pidog import Pidog; print('Official PiDog imported successfully')" 2>/dev/null; then
        print_success "✅ Official PiDog installation working"
    else
        print_error "❌ Official PiDog installation failed"
    fi
    deactivate
    
    # Test Custom version
    print_status "Testing Custom PiDog installation..."
    source "$CUSTOM_DIR/pidog/venv_custom/bin/activate"
    if python3 -c "from pidog import Pidog; print('Custom PiDog imported successfully')" 2>/dev/null; then
        print_success "✅ Custom PiDog installation working"
    else
        print_error "❌ Custom PiDog installation failed"
    fi
    deactivate
}

# Function to create usage instructions
create_usage_info() {
    print_header "Installation Complete!"
    
    cat << EOF
${GREEN}🎉 Both PiDog versions have been successfully installed!${NC}

${BLUE}Directory Structure:${NC}
$BASE_DIR/
├── Custom/
│   ├── pidog/                    # robopanda209 version
│   ├── robot-hat/                # dependencies
│   ├── vilib/
│   └── activate_custom.sh        # activation script
└── Official/
    ├── pidog/                    # official SunFounder version
    ├── robot-hat/                # dependencies
    ├── vilib/
    └── activate_official.sh      # activation script

${BLUE}Quick Start Commands:${NC}
${YELLOW}pidog-official${NC}     - Switch to official SunFounder version
${YELLOW}pidog-custom${NC}       - Switch to custom robopanda209 version
${YELLOW}pidog-help${NC}         - Show help information
${YELLOW}deactivate${NC}         - Exit current environment

${BLUE}Manual Activation:${NC}
source $OFFICIAL_DIR/activate_official.sh
source $CUSTOM_DIR/activate_custom.sh

${BLUE}Example Usage:${NC}
$ pidog-official
🤖 Official PiDog environment activated
📁 Working directory: $OFFICIAL_DIR/pidog
$ python3 your_script.py
$ deactivate

${GREEN}Happy coding with PiDog! 🐕${NC}
EOF
}

# Main installation function
main() {
    print_header "PiDog Dual Installation Script"
    print_status "This script will install both Official and Custom PiDog versions"
    print_status "Installation directory: $BASE_DIR"
    
    # Confirmation
    read -p "Continue with installation? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        print_status "Installation cancelled"
        exit 0
    fi
    
    # Check for required commands
    if ! command_exists git; then
        print_error "git is not installed. Please install git first."
        exit 1
    fi
    
    if ! command_exists python3; then
        print_error "python3 is not installed. Please install python3 first."
        exit 1
    fi
    
    # Run installation steps
    install_system_deps
    create_directories
    
    # Clone repositories
    clone_repo "$OFFICIAL_REPO" "$OFFICIAL_DIR/pidog" "Official PiDog"
    clone_repo "$CUSTOM_REPO" "$CUSTOM_DIR/pidog" "Custom PiDog"
    
    # Setup environments
    setup_environment "$OFFICIAL_DIR/pidog/venv_official" "Official" "$OFFICIAL_DIR/pidog" "$OFFICIAL_DIR"
    setup_environment "$CUSTOM_DIR/pidog/venv_custom" "Custom" "$CUSTOM_DIR/pidog" "$CUSTOM_DIR"
    
    # Create scripts and aliases
    create_activation_scripts
    add_aliases
    
    # Test installations
    test_installations
    
    # Show usage information
    create_usage_info
    
    print_success "Installation script completed!"
}

# Error handling
trap 'print_error "Installation failed at line $LINENO. Exit code: $?"' ERR

# Run main function
main "$@"