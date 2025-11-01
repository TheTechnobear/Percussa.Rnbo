#!/usr/bin/env python3
"""
check.py - Environment and project checker for Percussa RNBO

This script checks:
1. Required development tools installation
2. Environment variables and toolchain setup
3. Existing modules and their RNBO export status
4. Provides next step recommendations

Compatible with Windows, macOS, and Linux.
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


class EnvironmentChecker:
    def __init__(self):
        self.system = platform.system()
        self.is_macos = self.system == "Darwin"
        self.is_linux = self.system == "Linux"
        self.is_windows = self.system == "Windows"
        self.project_root = Path(__file__).parent.parent
        self.issues = []
        self.warnings = []
        self.successes = []

    def log_success(self, message):
        """Log a successful check"""
        self.successes.append("OK " + message)

    def log_warning(self, message):
        """Log a warning"""
        self.warnings.append("WARN " + message)

    def log_issue(self, message):
        """Log an issue"""
        self.issues.append("FAIL " + message)

    def check_command(self, command, version_arg="--version"):
        """Check if a command is available and return its version info"""
        try:
            result = subprocess.run([command, version_arg], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                self.log_success(command + " found: " + version)
                return True
            else:
                self.log_issue(command + " not working properly")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            self.log_issue(command + " not found")
            return False

    def check_basic_tools(self):
        """Check for basic development tools"""
        print("Checking basic development tools...")
        
        required_tools = ["cmake", "git"]
        optional_tools = ["python3", "python"]
        
        all_good = True
        for tool in required_tools:
            if not self.check_command(tool):
                all_good = False
        
        # Check Python (either python3 or python)
        python_found = False
        for py_cmd in optional_tools:
            if self.check_command(py_cmd):
                python_found = True
                break
        
        if not python_found:
            self.log_issue("Python not found (needed for scripts)")
            all_good = False
        
        return all_good

    def check_compiler_tools(self):
        """Check for compilation tools specific to platform"""
        print("\nChecking compilation tools...")
        
        if self.is_windows:
            self.log_issue("Windows is not supported for cross-compilation")
            return False
        
        all_good = True
        
        if self.is_macos:
            # Check for clang and llvm tools
            tools = ["clang", "clang++"]
            for tool in tools:
                if not self.check_command(tool):
                    all_good = False
            
            # Check if homebrew LLVM is available
            homebrew_paths = ["/opt/homebrew/opt/llvm/bin", "/usr/local/opt/llvm/bin"]
            llvm_found = False
            for path in homebrew_paths:
                if Path(path).exists():
                    self.log_success("LLVM tools found at " + path)
                    llvm_found = True
                    break
            
            if not llvm_found:
                self.log_warning("Homebrew LLVM not found. Install with: brew install llvm")
            
        elif self.is_linux:
            # Check for cross-compilation tools
            tools = ["clang", "clang++", "arm-linux-gnueabihf-gcc"]
            for tool in tools:
                if not self.check_command(tool):
                    all_good = False
        
        return all_good

    def check_environment_variables(self):
        """Check for required environment variables"""
        print("\nChecking environment variables...")
        
        # Check SSP_BUILDROOT
        ssp_buildroot = os.environ.get('SSP_BUILDROOT')
        if ssp_buildroot:
            ssp_path = Path(ssp_buildroot)
            if ssp_path.exists():
                # Check for expected subdirectories
                expected_paths = [
                    ssp_path / "arm-rockchip-linux-gnueabihf" / "sysroot",
                    ssp_path / "lib" / "gcc" / "arm-rockchip-linux-gnueabihf"
                ]
                if all(p.exists() for p in expected_paths):
                    self.log_success("SSP_BUILDROOT valid: " + ssp_buildroot)
                else:
                    self.log_warning("SSP_BUILDROOT path exists but missing expected subdirectories: " + ssp_buildroot)
            else:
                self.log_issue("SSP_BUILDROOT path does not exist: " + ssp_buildroot)
        else:
            # Check default location
            default_path = Path.home() / "buildroot" / "arm-rockchip-linux-gnueabihf_sdk-buildroot"
            if default_path.exists():
                self.log_success("Default SSP buildroot found: " + str(default_path))
                self.log_warning("Consider setting SSP_BUILDROOT environment variable")
            else:
                self.log_issue("SSP_BUILDROOT not set and default location not found")
                self.log_issue("Download from: https://sw13072022.s3.us-west-1.amazonaws.com/arm-rockchip-linux-gnueabihf_sdk-buildroot.tar.gz")

        # Check XMX_BUILDROOT (optional)
        xmx_buildroot = os.environ.get('XMX_BUILDROOT')
        if xmx_buildroot:
            xmx_path = Path(xmx_buildroot)
            if xmx_path.exists():
                expected_paths = [
                    xmx_path / "aarch64-rockchip-linux-gnu" / "sysroot",
                    xmx_path / "lib" / "gcc" / "aarch64-rockchip-linux-gnu"
                ]
                if all(p.exists() for p in expected_paths):
                    self.log_success("XMX_BUILDROOT valid: " + xmx_buildroot)
                else:
                    self.log_warning("XMX_BUILDROOT path exists but missing expected subdirectories: " + xmx_buildroot)
            else:
                self.log_issue("XMX_BUILDROOT path does not exist: " + xmx_buildroot)
        else:
            self.log_warning("XMX_BUILDROOT not set (only needed for XMX builds)")

    def check_project_structure(self):
        """Check project structure and dependencies"""
        print("\nChecking project structure...")
        
        # Check key directories and files
        key_paths = [
            ("CMakeLists.txt", "file"),
            ("juce", "dir"),
            ("ssp-sdk", "dir"),
            ("modules", "dir"),
            ("template/module", "dir"),
            ("scripts/createModule.py", "file"),
            ("scripts/addDemo.py", "file"),
        ]
        
        all_good = True
        for path_str, path_type in key_paths:
            path = self.project_root / path_str
            if path_type == "file" and path.is_file():
                self.log_success("Found " + path_str)
            elif path_type == "dir" and path.is_dir():
                self.log_success("Found " + path_str + "/")
            else:
                self.log_issue("Missing " + path_str)
                all_good = False
        
        # Check if JUCE submodule is initialized
        juce_cmake = self.project_root / "juce" / "CMakeLists.txt"
        if juce_cmake.exists():
            self.log_success("JUCE submodule initialized")
        else:
            self.log_issue("JUCE submodule not initialized")
            self.log_issue("Run: git submodule update --init --recursive")
            all_good = False
        
        return all_good

    def find_modules(self):
        """Find all existing modules and check their status"""
        modules_dir = self.project_root / "modules"
        modules = []
        
        if not modules_dir.exists():
            return modules
        
        for item in modules_dir.iterdir():
            if item.is_dir() and item.name not in ["common", "inc", ".gitignore"]:
                module_info = {
                    "name": item.name,
                    "path": item,
                    "has_source": False,
                    "has_rnbo_export": False,
                    "rnbo_export_path": None,
                    "missing_files": []
                }
                
                # Check for Source directory
                source_dir = item / "Source"
                if source_dir.exists():
                    module_info["has_source"] = True
                else:
                    module_info["missing_files"].append("Source/")
                
                # Check for RNBO export - try different naming patterns
                possible_rnbo_dirs = [
                    item / f"{item.name}-rnbo",
                    item / f"{item.name}-export", 
                    item / "rnbo-export",
                    item / "export"
                ]
                
                for rnbo_dir in possible_rnbo_dirs:
                    if rnbo_dir.exists():
                        module_info["rnbo_export_path"] = rnbo_dir
                        # Check for key RNBO files
                        rnbo_files = list(rnbo_dir.glob("*.cpp.h"))
                        if rnbo_files:
                            module_info["has_rnbo_export"] = True
                        break
                
                if not module_info["has_rnbo_export"]:
                    module_info["missing_files"].append(item.name + "-rnbo/ (with .cpp.h files)")
                
                modules.append(module_info)
        
        return modules

    def check_modules(self):
        """Check existing modules and their status"""
        print("\nChecking existing modules...")
        
        modules = self.find_modules()
        
        if not modules:
            self.log_warning("No modules found")
            return
        
        for module in modules:
            if module["has_source"] and module["has_rnbo_export"]:
                self.log_success("Module " + module['name'] + " is complete")
            elif module["has_source"]:
                self.log_warning("Module " + module['name'] + " missing RNBO export")
            else:
                self.log_issue("Module " + module['name'] + " incomplete: missing " + ', '.join(module['missing_files']))

    def suggest_next_steps(self):
        """Suggest next steps based on current state"""
        print("\nNext Steps:")
        
        modules = self.find_modules()
        
        if self.issues:
            print("\nCRITICAL ISSUES - Fix these first:")
            for issue in self.issues:
                print("   " + issue)
            print("\n   See setup guide: docs/setup.md")
            return
        
        if self.warnings:
            print("\nWARNINGS - Consider addressing:")
            for warning in self.warnings:
                print("   " + warning)
        
        print("\nEnvironment looks good!")
        
        if not modules:
            print("\nRECOMMENDED: Start with the demo")
            print("   python scripts/addDemo.py")
            print("   mkdir build && cd build && cmake .. && cmake --build .")
            print("   python scripts/removeModule.py DEMO --force")
            
        else:
            incomplete_modules = [m for m in modules if not (m["has_source"] and m["has_rnbo_export"])]
            complete_modules = [m for m in modules if m["has_source"] and m["has_rnbo_export"]]
            
            if incomplete_modules:
                print("\nCOMPLETE THESE MODULES:")
                for module in incomplete_modules:
                    if not module["has_rnbo_export"]:
                        print("   " + module['name'] + ": Export RNBO patch to " + module['name'] + "-rnbo/")
                        print("      Max → Export C++ Source Code → modules/" + module['name'] + "/" + module['name'] + "-rnbo/")
            
            if complete_modules:
                print("\nBUILD READY MODULES:")
                for module in complete_modules:
                    print("   " + module['name'] + ": Ready to build")
                
                print("\n   Build commands:")
                print("   mkdir build && cd build")
                print("   cmake ..                                    # Local VST3 testing")
                print("   cmake -DCMAKE_TOOLCHAIN_FILE=../xcSSP.cmake ..  # SSP hardware")
                print("   cmake --build .")
        
        print("\nCREATE NEW MODULE:")
        print("   python scripts/createModule.py YOUR_NAME")
        
        print("\nFull documentation: docs/creatingmodules.md")

    def run(self):
        """Run all checks and provide summary"""
        print("Percussa RNBO Environment Checker")
        print("=" * 50)
        
        self.check_basic_tools()
        self.check_compiler_tools()
        self.check_environment_variables()
        self.check_project_structure()
        self.check_modules()
        
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        
        if self.successes:
            print("\n[OK] " + str(len(self.successes)) + " items OK:")
            for success in self.successes:
                print("   " + success)
        
        if self.warnings:
            print("\n[WARN] " + str(len(self.warnings)) + " warnings:")
            for warning in self.warnings:
                print("   " + warning)
        
        if self.issues:
            print("\n[FAIL] " + str(len(self.issues)) + " issues:")
            for issue in self.issues:
                print("   " + issue)
        
        self.suggest_next_steps()
        
        return len(self.issues) == 0


def main():
    """Main entry point"""
    checker = EnvironmentChecker()
    success = checker.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()