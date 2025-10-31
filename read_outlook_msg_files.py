import extract_msg
import re
import os
import gc
dir = r"C:\Temp\Emails"

def process_msg_file(fullpath, partial_word):
    msg = extract_msg.Message(fullpath)
    msg_message = msg.body
    matches = re.findall(r'\b\w*' + re.escape(partial_word) + r'\w*\b', msg_message)
    del msg  # Explicitly delete to release file handle
    gc.collect()
    return matches

for dirpath, _, filenames in os.walk(dir):
        old_text = r"Action Required_ Welcome to the"
        
        for filename in filenames:
            if old_text in filename:
                old_path = os.path.join(dirpath, filename)
                print('Processing file>> ' + old_path)

                # Process the .msg file and extract the match
                partial_word = "navigator_perftest_"
                matches = process_msg_file(old_path, partial_word)

                if matches:
                    new_text = 'Email_for_' + matches[0]
                    new_filename = filename.replace(old_text, new_text)
                    new_path = os.path.join(dirpath, new_filename)

                    os.rename(old_path, new_path)
                    print(f'Renamed: {old_path} -> {new_path}')


# Output the matches
# print("Words containing the partial word:")
# for match in matches:
#     print(match)
