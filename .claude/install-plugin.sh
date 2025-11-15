#!/bin/bash

# CopilotKit Expert Plugin Installer
# Version: 1.0.0
#
# This script installs the CopilotKit Expert Plugin to another repository
# or exports it for distribution.

set -e

PLUGIN_NAME="copilotkit-expert"
VERSION="1.0.0"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Plugin files to install
PLUGIN_FILES=(
    "skills/copilotkit-expert.md"
    "commands/copilotkit-docs.md"
    "commands/copilotkit-integrate.md"
    "commands/copilotkit-debug.md"
    "copilotkit-patterns.md"
    "COPILOTKIT_PLUGIN.md"
    "MCP_SETUP.md"
    "QUICKSTART.md"
)

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to show usage
show_usage() {
    cat <<EOF
CopilotKit Expert Plugin Installer v${VERSION}

Usage:
    $0 [command] [options]

Commands:
    install <target-dir>    Install plugin to target repository
    export <output-dir>     Export plugin as standalone package
    verify                  Verify plugin installation in current repo
    help                    Show this help message

Examples:
    # Install to another repository
    $0 install /path/to/other/repo

    # Export as package
    $0 export /tmp/copilotkit-plugin

    # Verify current installation
    $0 verify

EOF
}

# Function to verify plugin files exist
verify_plugin() {
    print_info "Verifying CopilotKit Expert Plugin installation..."

    local missing_files=0
    local source_dir="${1:-.}"

    for file in "${PLUGIN_FILES[@]}"; do
        if [ -f "${source_dir}/.claude/${file}" ]; then
            print_success "${file}"
        else
            print_error "${file} - MISSING"
            missing_files=$((missing_files + 1))
        fi
    done

    if [ $missing_files -eq 0 ]; then
        print_success "All plugin files present!"
        return 0
    else
        print_error "${missing_files} file(s) missing"
        return 1
    fi
}

# Function to install plugin to target directory
install_plugin() {
    local target_dir="$1"

    if [ -z "$target_dir" ]; then
        print_error "Target directory not specified"
        show_usage
        exit 1
    fi

    if [ ! -d "$target_dir" ]; then
        print_error "Target directory does not exist: $target_dir"
        exit 1
    fi

    print_info "Installing CopilotKit Expert Plugin to: $target_dir"

    # Create .claude directory structure
    mkdir -p "${target_dir}/.claude/skills"
    mkdir -p "${target_dir}/.claude/commands"

    # Copy plugin files
    local current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    for file in "${PLUGIN_FILES[@]}"; do
        local source="${current_dir}/${file}"
        local dest="${target_dir}/.claude/${file}"

        if [ -f "$source" ]; then
            cp "$source" "$dest"
            print_success "Installed: ${file}"
        else
            print_warning "Skipped (not found): ${file}"
        fi
    done

    print_success "Plugin installed successfully!"
    print_info ""
    print_info "Next steps:"
    print_info "1. Configure the VIBE CODING MCP:"
    print_info "   claude mcp add --transport sse copilotkit-mcp https://mcp.copilotkit.ai/sse"
    print_info ""
    print_info "2. Read the quickstart guide:"
    print_info "   ${target_dir}/.claude/QUICKSTART.md"
    print_info ""
    print_info "3. Try a slash command:"
    print_info "   /copilotkit-docs"
}

# Function to export plugin as standalone package
export_plugin() {
    local output_dir="$1"

    if [ -z "$output_dir" ]; then
        print_error "Output directory not specified"
        show_usage
        exit 1
    fi

    print_info "Exporting CopilotKit Expert Plugin to: $output_dir"

    # Create output directory structure
    mkdir -p "${output_dir}/.claude/skills"
    mkdir -p "${output_dir}/.claude/commands"

    # Copy plugin files
    local current_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    for file in "${PLUGIN_FILES[@]}"; do
        local source="${current_dir}/${file}"
        local dest="${output_dir}/.claude/${file}"

        if [ -f "$source" ]; then
            cp "$source" "$dest"
            print_success "Exported: ${file}"
        else
            print_warning "Skipped (not found): ${file}"
        fi
    done

    # Create installer script in package
    cp "${current_dir}/install-plugin.sh" "${output_dir}/install.sh"
    chmod +x "${output_dir}/install.sh"

    # Create README for package
    cat > "${output_dir}/README.md" <<EOF
# CopilotKit Expert Plugin

Version: ${VERSION}

A comprehensive, reusable Claude Code plugin that provides expert knowledge of:
- CopilotKit framework
- AG-UI integration
- LangGraph, LangChain, Anthropic SDK, OpenAI
- Human-in-the-loop workflows
- State management and streaming

## Installation

\`\`\`bash
# Copy the .claude directory to your project
cp -r .claude /path/to/your/project/

# Or use the installer
./install.sh install /path/to/your/project

# Configure the VIBE CODING MCP
claude mcp add --transport sse copilotkit-mcp https://mcp.copilotkit.ai/sse
\`\`\`

## Usage

See \`.claude/QUICKSTART.md\` for complete documentation.

### Quick Commands

- \`/copilotkit-docs\` - Search documentation
- \`/copilotkit-integrate\` - Integration guide
- \`/copilotkit-debug\` - Debug issues

### Expert Agent

Just ask CopilotKit questions and the expert agent activates automatically!

## Documentation

- [Plugin Documentation](.claude/COPILOTKIT_PLUGIN.md)
- [Quick Start Guide](.claude/QUICKSTART.md)
- [Patterns & Best Practices](.claude/copilotkit-patterns.md)
- [MCP Setup](.claude/MCP_SETUP.md)

## License

Part of BLOG-CANVAS-COPILOTkit project. Reusable across projects.

---

Built with ❤️ for the CopilotKit community
EOF

    print_success "Plugin exported successfully!"
    print_info ""
    print_info "Package created at: $output_dir"
    print_info "To install in another project:"
    print_info "  cd $output_dir"
    print_info "  ./install.sh install /path/to/target/repo"
}

# Main command dispatcher
case "${1:-}" in
    install)
        install_plugin "$2"
        ;;
    export)
        export_plugin "$2"
        ;;
    verify)
        verify_plugin
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        if [ -z "${1:-}" ]; then
            show_usage
        else
            print_error "Unknown command: $1"
            show_usage
            exit 1
        fi
        ;;
esac
