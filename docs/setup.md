# Setup Your Development Environment

**One-time setup** to prepare your computer for building SSP/XMX modules.

## Step 1: Install Development Tools

### macOS Users
```bash
# Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install cmake git llvm pkg-config arm-linux-gnueabihf-binutils

# Add to your shell config (.zshrc or .bashrc)
# Apple Silicon Macs:
export PATH=/opt/homebrew/bin:"${PATH}"

# Intel Macs:
export PATH=/usr/local/bin:"${PATH}"
```

### Linux Users
```bash
# Ubuntu/Debian
sudo apt install cmake git llvm clang g++-10-arm-linux-gnueabihf

# Other distros: use your package manager (pacman, yum, etc.)
```

### Windows Users
**Install Linux in a Virtual Machine** - Windows builds are not supported.

## Step 2: Download Build Tools

1. **Download the buildroot**:  
   SSP  : [arm-rockchip-linux-gnueabihf_sdk-buildroot.tar.gz](https://sw13072022.s3.us-west-1.amazonaws.com/arm-rockchip-linux-gnueabihf_sdk-buildroot.tar.gz)

   XMX  :  [aarch64-rockchip-linux-gnu_sdk-buildroot.tar.gz](https://sw13072022.s3.us-west-1.amazonaws.com/aarch64-rockchip-linux-gnu_sdk-buildroot.tar.gz)

2. **Extract to ~/buildroot**:
```bash
mkdir -p ~/buildroot/ssp
cd ~/buildroot/ssp
# Move your downloaded file here, then:
tar xzf arm-rockchip-linux-gnueabihf_sdk-buildroot.tar.gz

# mkdir -p ~/buildroot/xmx
# cd ~/buildroot/xmx
# tar xzf aarch64-rockchip-linux-gnu_sdk-buildroot.tar.gz

```

3. **Verify installation**:
```bash
ls ~/buildroot/ssp/arm-rockchip-linux-gnueabihf_sdk-buildroot/libexec
# Should show: awk c++-analyzer ccc-analyzer gcc

# ls ~/buildroot/xmx/aarch64-rockchip-linux-gnu_sdk-buildroot/libexec
```

4. **Configure environment variables**: (recommended)
```bash
# Add these to your shell config file (.zshrc, .bashrc, etc.)
export SSP_BUILDROOT="$HOME/buildroot/ssp/arm-rockchip-linux-gnueabihf_sdk-buildroot"

# For XMX support (if you have the XMX buildroot):
# export XMX_BUILDROOT="$HOME/buildroot/xmx/aarch64-rockchip-linux-gnu_sdk-buildroot"

# Reload your shell config
source ~/.zshrc  # or source ~/.bashrc
```

alternativly (not recommended), untar directly into ```~/buildroot``

**Why set these variables?**
- Ensures the build system finds your toolchains automatically
- Avoids "BUILDROOT environment variable missing" warnings
- Makes switching between SSP and XMX builds easier

## Step 4: Get This Project

```bash
# Create projects folder
mkdir ~/projects
cd ~/projects

# Download the project
git clone https://github.com/thetechnobear/PERCUSSA.RNBO
cd PERCUSSA.RNBO

# Download dependencies (JUCE framework)
git submodule update --init --recursive
```

## Step 5: Verify Your Environment

Before attempting to build anything, use the built-in environment checker:

```bash
# Check your complete development environment
python3 scripts/check.py
```

This script will verify:
- ✅ All required development tools are installed
- ✅ Toolchains and build environments are properly configured  
- ✅ Project structure and dependencies are complete
- ✅ Any existing modules and their status

**Fix any issues** reported by the checker before proceeding.

## Step 6: Test Your Setup

Create and build a demo module to verify everything works:

```bash
# Create a demo module with example RNBO code
python3 scripts/addDemo.py

# Build VST (this may take a few minutes the first time)
```bash
cmake --fresh -B build && cmake --build build 

# Build for SSP (optional, this may take a few minutes the first time)
cmake --fresh -B build.ssp -DCMAKE_TOOLCHAIN_FILE=../xcSSP.cmake && cmake --build build.ssp

# Build for XMX (optional, this may take a few minutes the first time)
cmake --fresh -B build.xmx -DCMAKE_TOOLCHAIN_FILE=../xcXMX.cmake && cmake --build build.xmx

# Clean up the demo
cd ..
python3 scripts/removeModule.py DEMO --force
```

## ✅ Success!

If the demo builds without errors, you're ready to create your own modules!

**Next step**: [Creating Modules](creatingmodules.md)

## Troubleshooting

**Environment issues?**
- Run `python3 scripts/check.py` to get a detailed status report
- The checker will identify specific problems and suggest solutions

**Build errors?** 
- Check that all tools are installed correctly
- Verify the buildroot path: `~/buildroot/arm-rockchip-linux-gnueabihf_sdk-buildroot/`
- Try the demo build first before creating custom modules
- Use the environment checker to validate your setup

**Need help?**
- Check the [Percussa forum](https://forum.percussa.com) for community support 


