
import os
import sys

# Add the 'dashboard' directory to the path so we can import ml_utils
sys.path.append(os.path.join(os.getcwd(), 'dashboard'))
# Also add the root project path
sys.path.append(os.getcwd())

# Mock Django setup implicitly or just try to import ml_utils relative to the script location
# ml_utils relies on 'pandas', 'sklearn' etc. which are installed.
# It does NOT import dango models at the top level, thankfully.

from dashboard import ml_utils

try:
    print("Testing load_and_train_models()...")
    ml_utils.load_and_train_models()
    
    print("\nTesting predict_score(3, 7, 5)...")
    score = ml_utils.predict_score(3, 7, 5)
    print(f"Predicted Score: {score}")
    
    if score > 0:
        print("\nSUCCESS: Model trained and prediction working.")
    else:
        print("\nWARNING: Prediction returned 0, might indicate model failure.")

except Exception as e:
    print(f"\nFAILURE: Helper script crashed: {e}")
    import traceback
    traceback.print_exc()
