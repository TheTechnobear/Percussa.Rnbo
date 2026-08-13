#!/usr/bin/env python3
"""
addDemo.py - Create a Demo module with example RNBO code

This script creates a Demo module by:
1. Creating a Demo module using createModule.py with default arguments
2. Copying demo RNBO code from template/Demo/Demo-rnbo to modules/Demo/Demo-rnbo
3. Providing a complete working example for testing

Compatible with Windows, macOS, and Linux.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory"""
    script_dir = Path(__file__).parent
    return script_dir.parent


def create_demo_module(project_root: Path) -> bool:
    """Create Demo module using createModule.py"""
    create_script = project_root / "scripts" / "createModule.py"
    
    if not create_script.exists():
        print(f"Error: createModule.py not found at {create_script}")
        return False
    
    # Build command line arguments for Demo module
    cmd = [
        sys.executable, str(create_script),
        "DEMO",  # module ID (must be uppercase)
        "--name", "Demo Module",
        "--description", "Demo module with example RNBO patch",
        "--brand", "Example",
        "--author", "Example Team",
        "--email", "info@example.com",
        "--website", "https://example.com"
    ]
    
    print("Creating DEMO module...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("Successfully created DEMO module")
            return True
        else:
            print("Failed to create DEMO module:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Error creating DEMO module: {e}")
        return False


def copy_demo_rnbo_code(project_root: Path) -> bool:
    """Copy demo RNBO code from template to module"""
    template_rnbo_dir = project_root / "template" / "Demo" / "Demo-rnbo"
    module_rnbo_dir = project_root / "modules" / "DEMO" / "DEMO-rnbo"
    
    # Validate source directory exists
    if not template_rnbo_dir.exists():
        print(f"Error: Template RNBO directory not found: {template_rnbo_dir}")
        return False
    
    # Validate destination directory exists (should be created by createModule.py)
    if not module_rnbo_dir.exists():
        print(f"Error: Module RNBO directory not found: {module_rnbo_dir}")
        print("Make sure the DEMO module was created successfully first.")
        return False
    
    print(f"Copying demo RNBO code from {template_rnbo_dir} to {module_rnbo_dir}")
    
    try:
        # Copy all files from template to module
        for item in template_rnbo_dir.iterdir():
            if item.is_file():
                dest_file = module_rnbo_dir / item.name
                shutil.copy2(item, dest_file)
                print(f"  Copied: {item.name}")
            elif item.is_dir():
                dest_dir = module_rnbo_dir / item.name
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                shutil.copytree(item, dest_dir)
                print(f"  Copied directory: {item.name}")
        
        print("Successfully copied demo RNBO code")
        return True
        
    except Exception as e:
        print(f"Error copying demo RNBO code: {e}")
        return False


def check_demo_exists(project_root: Path) -> bool:
    """Check if DEMO module already exists"""
    demo_dir = project_root / "modules" / "DEMO"
    return demo_dir.exists()


def print_success_message():
    """Print success message with next steps"""
    print("\n" + "=" * 60)
    print("DEMO module created successfully!")
    print("=" * 60)
    print("\nThe DEMO module includes:")
    print("  - Complete module structure")
    print("  - Example RNBO code ready to build")
    print("  - All placeholder substitutions")
    print("\nNext steps:")
    print("1. Build the DEMO module:")
    print("cmake --fresh -B build && cmake --build build")
    print("cmake --fresh -B build.ssp -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=./xcSSP.cmake && cmake --build build.ssp ")
    print("cmake --fresh -B build.xmx -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=./xcXMX.cmake && cmake --build build.xmx ")
    print("\n3. Remove the DEMO module when done:")
    print("   python scripts/removeModule.py DEMO")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create a DEMO module with example RNBO code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script creates a complete DEMO module including:
  - Module structure from template
  - Example RNBO code from template/Demo/Demo-rnbo
  - Ready-to-build configuration

The DEMO module provides:
  - A working example of RNBO integration
  - Complete build configuration
  - Reference implementation for development

Examples:
  # Create DEMO module
  python addDemo.py
  
  # Force recreate DEMO module (removes existing first)
  python addDemo.py --force
        """
    )
    
    parser.add_argument('--force', action='store_true',
                       help='Remove existing DEMO module and recreate it')
    
    args = parser.parse_args()
    
    # Get project root
    project_root = get_project_root()
    
    # Check if DEMO already exists
    if check_demo_exists(project_root):
        if args.force:
            print("DEMO module already exists. Removing it first...")
            remove_script = project_root / "scripts" / "removeModule.py"
            if remove_script.exists():
                try:
                    result = subprocess.run([
                        sys.executable, str(remove_script), "DEMO", "--force"
                    ], capture_output=True, text=True, cwd=project_root)
                    
                    if result.returncode != 0:
                        print("Failed to remove existing DEMO module:")
                        print(result.stderr)
                        sys.exit(1)
                    print("Existing DEMO module removed successfully")
                except Exception as e:
                    print(f"Error removing existing DEMO module: {e}")
                    sys.exit(1)
            else:
                print(f"Error: removeModule.py not found at {remove_script}")
                sys.exit(1)
        else:
            print("DEMO module already exists!")
            print("Use --force to remove and recreate it, or remove it manually:")
            print("  python scripts/removeModule.py DEMO")
            sys.exit(1)
    
    # Create DEMO module
    if not create_demo_module(project_root):
        print("Failed to create DEMO module")
        sys.exit(1)
    
    # Copy demo RNBO code
    if not copy_demo_rnbo_code(project_root):
        print("Failed to copy demo RNBO code")
        sys.exit(1)
    
    # Success!
    print_success_message()


if __name__ == "__main__":
    main()