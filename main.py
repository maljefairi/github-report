from utils import *
import openai
from dotenv import load_dotenv

load_dotenv()

# Get the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Call the function to remove previous output files
remove_previous_output('.')

SETTINGS_FILE = "settings.txt"
repository_path = '.'

try:
    all_file_types = get_file_types(repository_path)
except Exception as e:
    print(f"An error occurred while getting file types: {str(e)}")
    exit(1)

if os.path.isfile(SETTINGS_FILE):
    load_previous = input('Do you want to run with the previous settings? (y/n) ')
    if load_previous.lower() == 'y':
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
        included_file_types = settings['included_file_types']
        max_words = settings['max_words']
        include_tree = settings['include_tree']
        additional_text = settings['additional_text']
    else:
        included_file_types, max_words, include_tree, additional_text = ask_user_inputs(all_file_types, repository_path)
else:
    included_file_types, max_words, include_tree, additional_text = ask_user_inputs(all_file_types, repository_path)

ignore_patterns = parse_gitignore(repository_path)
all_files = get_all_files(repository_path, included_file_types, ignore_patterns)

for file_path, file_content in all_files:
    print(f"Processing file: {file_path}")
    if 'GPT' not in file_path:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": file_content}],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        improved_code = response['choices'][0]['message']['content']
        new_file = os.path.join(os.path.dirname(file_path), os.path.splitext(os.path.basename(file_path))[0] + 'GPT' + os.path.splitext(os.path.basename(file_path))[1])
        with open(new_file, 'w') as f:
            f.write(improved_code)

settings = {
    'included_file_types': included_file_types,
    'max_words': max_words,
    'include_tree': include_tree,
    'additional_text': additional_text,
}
with open(SETTINGS_FILE, 'w') as file:
    json.dump(settings, file)
