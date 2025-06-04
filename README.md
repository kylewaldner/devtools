# devtools

helpers for working on my projects

## Features

This devtools package includes:

- **tagger**: An intelligent Git tag manager that helps create semantic version tags with automatic version incrementing
- Easy PATH setup for shell integration

## Prerequisites

### System Requirements

- **Python 3.6+** (with standard library modules)
- **Git** (for the tagger tool)
- **Unix-like shell** (bash, zsh, fish, tcsh, or csh)

### Python Dependencies

This project uses only Python standard library modules:
- `argparse` - Command-line argument parsing
- `os` - Operating system interface
- `sys` - System-specific parameters and functions
- `subprocess` - Subprocess management
- `tempfile` - Temporary file and directory creation
- `pathlib` - Object-oriented filesystem paths
- `re` - Regular expression operations
- `signal` - Signal handling
- `typing` - Type hints support

**No external dependencies required** All functionality is built using Python's standard library.

## Installation

### Quick Install

Run the installation script to automatically add the tools to your PATH:

```bash
./install.py
```

### Installation Options

The installer supports several options:

```bash
# Install with automatic confirmation
./install.py -y

# Preview changes without applying them
./install.py --dry-run

# Get help
./install.py --help
```

### What the installer does

1. **Detects your shell** (bash, zsh, fish, tcsh, csh)
2. **Locates your shell's RC file** (`.bashrc`, `.zshrc`, etc.)
3. **Adds the tools directory to your PATH** by appending an export line
4. **Shows a diff** of changes before applying them
5. **Creates backups** and handles errors gracefully

### Supported Shells

- **bash** → `~/.bashrc`
- **zsh** → `~/.zshrc`
- **fish** → `~/.config/fish/config.fish`
- **tcsh** → `~/.tcshrc`
- **csh** → `~/.cshrc`

### Manual Installation

If you prefer to set up the PATH manually:

1. Add this line to your shell's RC file:
   ```bash
   export PATH="/path/to/devtools/tools:$PATH"
   ```

2. Reload your shell:
   ```bash
   source ~/.bashrc  # or your shell's RC file
   ```

## Tools

### tagger

An intelligent Git tag manager that simplifies version tagging workflows.

**Features:**
- Automatic semantic version increment (patch/minor/major)
- Interactive prompts with sensible defaults
- Tag validation and conflict detection
- Remote push management
- Comprehensive tag information display

**Usage:**
```bash
# Interactive mode (recommended)
tagger

# Quick tag creation
tagger -t "v1.2.3" -d "Release description"

# Auto-push to remote without prompting
tagger -p

# Increment major version
tagger --increment major
```

**Requirements:**
- Must be run in a Git repository
- Git must be installed and in PATH

## Verification

After installation, verify that the tools are available:

```bash
# Check if tagger is in PATH
which tagger

# Test tagger (must be in a Git repo)
tagger --help
```

## Troubleshooting

### PATH not updated
- Restart your terminal or run `source ~/.bashrc` (or your shell's RC file)
- Check that the export line was added correctly to your RC file

### Permission errors
- Ensure you have write permissions to your home directory
- The tools directory should be readable and executable

### Git repository errors
- The `tagger` tool must be run from within a Git repository
- Ensure Git is installed and properly configured

## Uninstall

To remove devtools from your PATH:

1. Edit your shell's RC file and remove the line containing the devtools path
2. Restart your terminal or reload your shell configuration

## License

This project is licensed under the terms in the LICENSE file.
