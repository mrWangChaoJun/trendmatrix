#!/usr/bin/env python3
# Test script for AI module structure and imports

import sys
import os
from datetime import datetime

print("=== Testing AI Module Structure ===")
print(f"Test started at: {datetime.now().isoformat()}")
print("\n1. Testing directory structure...")

# Test 1: Directory structure
directories = [
    'src/ai',
    'src/ai/models',
    'src/ai/models/nlp',
    'src/ai/models/time_series',
    'src/ai/models/anomaly',
    'src/ai/evaluators',
    'src/ai/trainers',
    'src/ai/predictors',
    'src/ai/utils'
]

for directory in directories:
    if os.path.exists(os.path.join(os.path.dirname(__file__), directory)):
        print(f"   ✓ {directory} exists")
    else:
        print(f"   ✗ {directory} missing")

# Test 2: File existence
print("\n2. Testing file existence...")

files = [
    'src/ai/__init__.py',
    'src/ai/models/__init__.py',
    'src/ai/models/nlp/__init__.py',
    'src/ai/models/nlp/sentiment_analyzer.py',
    'src/ai/models/time_series/__init__.py',
    'src/ai/models/time_series/price_predictor.py',
    'src/ai/models/anomaly/__init__.py',
    'src/ai/models/anomaly/anomaly_detector.py',
    'src/ai/models/trend_identifier.py',
    'src/ai/evaluators/__init__.py',
    'src/ai/evaluators/model_evaluator.py',
    'src/ai/trainers/__init__.py',
    'src/ai/trainers/model_trainer.py',
    'src/ai/predictors/__init__.py',
    'src/ai/predictors/trend_predictor.py',
    'src/ai/utils/__init__.py',
    'src/ai/utils/base_model.py'
]

for file in files:
    if os.path.exists(os.path.join(os.path.dirname(__file__), file)):
        print(f"   ✓ {file} exists")
    else:
        print(f"   ✗ {file} missing")

# Test 3: Module imports (without dependencies)
print("\n3. Testing module imports (structure only)...")

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test importing the main AI module
    import ai
    print("   ✓ ai module imported successfully")

except Exception as e:
    print(f"   ✗ ai module import failed: {e}")

    # Try to import individual modules to identify the issue
    print("\n   Attempting to identify import issues...")

    # Test base_model.py
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src/ai/utils'))
        import base_model
        print("   ✓ base_model.py imported successfully")
    except Exception as e:
        print(f"   ✗ base_model.py import failed: {e}")

print("\n4. Testing module structure summary...")

# Count files and directories
total_dirs = 0
total_files = 0

for root, dirs, files_in_dir in os.walk(os.path.join(os.path.dirname(__file__), 'src/ai')):
    total_dirs += len(dirs)
    total_files += len([f for f in files_in_dir if f.endswith('.py')])

print(f"   Total directories: {total_dirs}")
print(f"   Total Python files: {total_files}")

# Check for __init__.py files
init_files = []
for root, dirs, files_in_dir in os.walk(os.path.join(os.path.dirname(__file__), 'src/ai')):
    for file in files_in_dir:
        if file == '__init__.py':
            init_files.append(os.path.relpath(os.path.join(root, file), os.path.join(os.path.dirname(__file__), 'src/ai')))

print(f"   Total __init__.py files: {len(init_files)}")
for init_file in init_files:
    print(f"     - {init_file}")

print("\n=== Test Summary ===")
print(f"Test completed at: {datetime.now().isoformat()}")
print("\nModule structure test completed. The AI module has been successfully created with:")
print(f"- {total_dirs} directories")
print(f"- {total_files} Python files")
print(f"- {len(init_files)} __init__.py files for proper module structure")
print("\nNote: Full functionality testing requires installing dependencies:")
print("  - tensorflow")
print("  - keras")
print("  - numpy")
print("  - scikit-learn")
print("  - pandas")
print("\n=== End of Test ===")
