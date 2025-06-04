#!/usr/bin/env python3
"""
Script to add the tools directory to PATH by updating the shell's rc file.
"""

import argparse
import os
import sys
import subprocess
import tempfile
from pathlib import Path


def get_shell_and_rc_file():
    """Determine the current shell and its corresponding rc file."""
    shell = os.environ.get('SHELL', '/bin/bash')
    shell_name = Path(shell).name
    
    home = Path.home()
    
    rc_files = {
        'bash': home / '.bashrc',
        'zsh': home / '.zshrc',
        'fish': home / '.config' / 'fish' / 'config.fish',
        'tcsh': home / '.tcshrc',
        'csh': home / '.cshrc',
    }
    
    rc_file = rc_files.get(shell_name, home / '.bashrc')
    
    return shell_name, rc_file


def get_tools_path():
    """Get the absolute path to the tools directory."""
    script_dir = Path(__file__).parent.absolute()
    tools_dir = script_dir / 'tools'
    return tools_dir


def create_path_export_line(shell_name, tools_path):
    """Create the appropriate export line for the shell."""
    if shell_name == 'fish':
        return f'set -gx PATH "{tools_path}" $PATH\n'
    else:
        return f'export PATH="{tools_path}:$PATH"\n'


def path_already_added(rc_file, tools_path):
    """Check if the tools path is already in the rc file."""
    if not rc_file.exists():
        return False
    
    content = rc_file.read_text()
    return str(tools_path) in content


def show_diff(original_content, new_content, rc_file):
    """Show a diff of the changes to be made."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.orig', delete=False) as orig_file:
        orig_file.write(original_content)
        orig_file.flush()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.new', delete=False) as new_file:
            new_file.write(new_content)
            new_file.flush()
            
            try:
                # Try to use diff command for better output
                result = subprocess.run([
                    'diff', '-u', '--color=auto',
                    '--label', f'{rc_file} (original)',
                    '--label', f'{rc_file} (modified)',
                    orig_file.name, new_file.name
                ], capture_output=True, text=True)
                
                if result.stdout:
                    print("Changes to be made:")
                    print(result.stdout)
                else:
                    print("No changes detected.")
                    
            except FileNotFoundError:
                # Fallback if diff command is not available
                print("Changes to be made:")
                print(f"--- {rc_file} (original)")
                print(f"+++ {rc_file} (modified)")
                
                orig_lines = original_content.splitlines()
                new_lines = new_content.splitlines()
                
                if len(new_lines) > len(orig_lines):
                    print(f"@@ -{len(orig_lines)},0 +{len(orig_lines)},1 @@")
                    for line in new_lines[len(orig_lines):]:
                        print(f"+{line}")
            
            finally:
                os.unlink(orig_file.name)
                os.unlink(new_file.name)


def main():
    parser = argparse.ArgumentParser(
        description='Add the tools directory to PATH by updating shell rc file.'
    )
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Skip confirmation prompt and apply changes automatically'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making any modifications'
    )
    
    args = parser.parse_args()
    
    # Get shell info and tools path
    shell_name, rc_file = get_shell_and_rc_file()
    tools_path = get_tools_path()
    
    print(f"Detected shell: {shell_name}")
    print(f"RC file: {rc_file}")
    print(f"Tools directory: {tools_path}")
    
    # Check if tools directory exists
    if not tools_path.exists():
        print(f"Warning: Tools directory '{tools_path}' does not exist.")
        if not args.yes:
            response = input("Continue anyway? (y/n): ")
            if response.lower() not in ('y', 'yes'):
                print("Aborted.")
                return 1
    
    # Check if already added
    if path_already_added(rc_file, tools_path):
        print(f"Tools path is already present in {rc_file}")
        return 0
    
    # Read current content
    if rc_file.exists():
        original_content = rc_file.read_text()
    else:
        original_content = ""
        print(f"RC file {rc_file} does not exist. It will be created.")
    
    # Create new content
    export_line = create_path_export_line(shell_name, tools_path)
    
    if original_content and not original_content.endswith('\n'):
        new_content = original_content + '\n' + export_line
    else:
        new_content = original_content + export_line
    
    # Show diff
    show_diff(original_content, new_content, rc_file)
    
    if args.dry_run:
        print("\nDry run mode: no changes were made.")
        return 0
    
    # Get confirmation
    if not args.yes:
        response = input("\nApply these changes? (y/n): ")
        if response.lower() not in ('y', 'yes'):
            print("Aborted.")
            return 0
    
    # Create parent directory if it doesn't exist (for fish config)
    rc_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the changes
    try:
        rc_file.write_text(new_content)
        print(f"Successfully updated {rc_file}")
        print(f"\nTo apply the changes immediately, run:")
        if shell_name == 'fish':
            print(f"  source {rc_file}")
        else:
            print(f"  source {rc_file}")
        print("Or restart your shell.")
        
    except Exception as e:
        print(f"Error writing to {rc_file}: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main()) 