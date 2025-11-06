import os
import shutil

# --- CONFIGURATION ---
wav_folder = 'wav'
transcript_folder = 'transcripts'
output_corpus_folder = 'mfa_corpus'
# ---------------------

# Create the output directory if it doesn't exist
os.makedirs(output_corpus_folder, exist_ok=True)

print(f"Starting data preparation...")
print(f"Audio source: {wav_folder}")
print(f"Transcript source: {transcript_folder}")
print(f"Output corpus: {output_corpus_folder}")

file_count = 0
errors = []

# Iterate through the transcript files
for transcript_filename in os.listdir(transcript_folder):
    
    # --- THIS IS THE FIX ---
    # Check for .txt or .TXT (case-insensitive)
    if transcript_filename.lower().endswith('.txt'):
        
        # Get the base name (e.g., "F2BJRLP1")
        base_name = os.path.splitext(transcript_filename)[0]
        
        # Define paths
        txt_path = os.path.join(transcript_folder, transcript_filename)
        wav_path = os.path.join(wav_folder, base_name + '.wav')
        
        # Define output paths
        out_wav_path = os.path.join(output_corpus_folder, base_name + '.wav')
        out_lab_path = os.path.join(output_corpus_folder, base_name + '.lab') # MFA prefers .lab
        
        # Check if the matching wav file exists
        if not os.path.exists(wav_path):
            print(f"Error: Missing WAV file for transcript {transcript_filename}")
            errors.append(base_name)
            continue
            
        try:
            # 1. Copy the WAV file
            shutil.copyfile(wav_path, out_wav_path)
            
            # 2. Read the transcript content
            with open(txt_path, 'r', encoding='utf-8') as f:
                transcript_text = f.read().strip()
                
            # 3. Write the new .lab file
            # MFA expects transcripts to be ALL CAPS for ARPA models
            with open(out_lab_path, 'w', encoding='utf-8') as f:
                f.write(transcript_text.upper())
                
            file_count += 1
            
        except Exception as e:
            print(f"Error processing {base_name}: {e}")
            errors.append(base_name)

print("\n--- Preparation Complete ---")
print(f"Successfully processed {file_count} file pairs.")
if errors:
    print(f"Failed to process {len(errors)} files. Please check:")
    for error in errors:
        print(f"- {error}")