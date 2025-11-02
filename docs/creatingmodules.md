# Creating Your RNBO Modules

Turn your Max RNBO patches into SSP/XMX modules using simple Python scripts.

**Prerequisites**: Complete the [setup process](setup.md) first.

## Option 1: Try the Demo (Recommended First Step)

Test your setup with a working example:

```bash
# Create demo module with example RNBO code
python3 scripts/addDemo.py

# Build for testing on your computer (VST3)
mkdir build
cd build
cmake ..
cmake --build .

# The demo creates a 4-channel attenuator module
# Find DEMO.vst3 in build/modules/DEMO/DEMO_artefacts/
```

## Option 2: Create Your Own Module

### Step 1: Create Module Structure

Use the interactive script:
```bash
python3 scripts/createModule.py
```

Or specify details directly:
```bash
python3 scripts/createModule.py VERB --name "My Reverb" --description "Lush reverb effect" --author "Your Name"
```

**Requirements**:
- Module ID: **Exactly 4 uppercase letters/numbers** (e.g., VERB, DLY1, FILT)
- Must start with a letter
- Each module needs a unique ID

### Step 2: Export Your RNBO Patch

In Max, export your RNBO patch with these **exact settings**:

**For module named "RVRB":**
- **Export Type**: C++ 
- **Output Directory**: `modules/RVRB/RVRB-rnbo/` 
- **Export Name**: `RVRB.cpp.h`
- **Codegen Class Name**: `RVRBRnbo`
- **Export Options**:
  - ✅ Minimal Export
  - ❌ Copy C++ library code

⚠️ **Critical**: Codegen class name must be `[ModuleId]Rnbo`


### Step 3: Build Your Module

**For testing on your computer (VST3)**:
```bash
cmake --fresh -B build && cmake --build build 
```
susequent builds can be done with `` cmake --build build```

**For SSP hardware**:
```bash
cmake --fresh -B build.ssp -DCMAKE_TOOLCHAIN_FILE=../xcSSP.cmake && cmake --build build.ssp
```

**For XMX hardware**:
```bash
cmake --fresh -B build.xmx -DCMAKE_TOOLCHAIN_FILE=../xcXMX.cmake && cmake --build build.xmx
```

subsequent builds can be done with  ```cmake --build build.ssp``` or ```cmake --build build.xmx```

### Step 4: Install Your Module

**Testing (VST3)**: 
- Find your `.vst3` file in `build/modules/YOUR_MODULE/YOUR_MODULE_artefacts/`
- Load in any VST3 host (try JUCE AudioPluginHost)

**SSP/XMX Hardware**:
plugin file will be located in artifacts : 
e.g for demo : 
``` modules/DEMO/DEMO_artefacts/Release/VST3/DEMO.vst3/Contents/armv7l-linux/DEMO.so```
or 
```modules/DEMO/DEMO_artefacts/Release/VST3/DEMO.vst3/Contents/armv7l-linux/DEMO.so```

- Copy the .so file to SSP/XMX SD card in the `plugins` folder

## Managing Modules

### List All Modules
```bash
python3 scripts/removeModule.py --list
```

### Remove a Module
```bash
python3 scripts/removeModule.py YOUR_MODULE
```

## Building Tips


### Performance Tips

- **First build**: Takes several minutes (compiling JUCE framework)
- **Subsequent builds**: Much faster (only your changes)
- **Clean builds**: Delete build folders and start fresh if you have issues

### Troubleshooting

**Module won't build?**
- Check that your RNBO export is in the correct folder
- Verify your module ID is exactly 4 characters, uppercase, starts with letter
- Try building the demo first to test your setup

**RNBO export issues?**
- Make sure you export "C++ Source Code" (not other formats) with settings as detailed above
- Export the entire contents to the module's RNBO folder
- Check that files like `description.json` and `.cpp.h` files are present

**Need to start over?**
```bash
# Remove your module and try again
python3 scripts/removeModule.py YOUR_MODULE --force
python3 scripts/createModule.py YOUR_MODULE
```

## What Gets Created

When you create a module, you get:

```
modules/YOUR_MODULE/
├── CMakeLists.txt           # Build configuration  
├── Source/                  # Plugin source code
│   ├── PluginProcessor.cpp  # Main audio processing
│   ├── PluginEditor.cpp     # Full SSP interface
│   └── PluginMiniEditor.cpp # Compact XMX interface
└── YOUR_MODULE-rnbo/        # YOUR RNBO EXPORT GOES HERE
    ├── description.json     # RNBO patch info
    ├── YOUR_MODULE.cpp.h     # RNBO generated code
    └── dependencies.json    # RNBO dependencies
```

The template automatically:
- ✅ Detects your RNBO parameters and creates SSP controls
- ✅ Sets up audio input/output based on your patch
- ✅ Handles SSP-specific display and interaction
- ✅ Creates both full SSP and compact XMX interfaces

**Next**: Start with the demo, then create your first module!





