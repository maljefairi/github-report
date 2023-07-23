# Repository Code Review and Refactoring with GPT-4

This project is designed to automatically review and suggest improvements to code files within your repositories by leveraging the power of OpenAI's GPT-4 model. This tool will ensure your code adheres to industry-standard practices and is efficient in terms of functionality.

## Project Summary

This project, known as the "GPT-4 Code Reviewer and Improver", is designed to help developers improve the quality of their code. It works by automatically scanning selected files in a repository, sending the code in these files to OpenAI's GPT-4 model, and then providing the developer with suggestions for improvements and optimizations. 

The GPT-4 model can offer insights into potential coding issues, propose more efficient ways to write certain sections of code, and even offer suggestions for adhering to best practices and coding standards. 

In this project, a special emphasis has been placed on reusability and efficiency. It maintains a record of previously processed files to prevent redundant reviews. The processed code is saved with a distinct naming convention to distinguish it from the original code.

The project is built with Python and relies heavily on OpenAI's GPT-4 model, making it a great example of how AI can assist in software development tasks. The project uses an .env file for securely storing API keys, enhancing its security posture. 

This project is a great tool for both individual developers looking to improve their code, and teams that want to ensure a uniform coding standard across their project. 

Please note that usage of OpenAI's GPT-4 requires API access which might have associated costs as per OpenAI's pricing policy. 

The software is released under the MIT license, allowing for free use, modification, distribution, and private use. Enjoy and happy coding!

## Prerequisites

- Python 3.6+
- OpenAI Python
- python-dotenv

Additionally, you'll need an OpenAI account to access the GPT-4 model and retrieve your API key.

## Installation

1. Clone the repository:

```sh
git clone https://github.com/your_username/your_project.git
```

2. Install the required packages:

```sh
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:

```sh
OPENAI_API_KEY=your_api_key
```

## Usage

There are two Python scripts that run the operations:

1. `main.py`: This is the driver script that uses your OpenAI API key to interact with the GPT-4 model. It identifies eligible files in your repository and sends their contents for review. The refactored code is then saved with the same filename (appended by 'GPT') at the same location in your repository.

2. `utils.py`: This file houses several utility functions used by the `main.py`. These include getting all files, parsing the `.gitignore` file, splitting the text, and more.

To run the script:

```sh
python main.py
```

## Disclaimer

The code is theoretical and works under the assumption that OpenAI's GPT-4 model can offer improvements to your code. As AI models may not completely grasp programming semantics and best practices, we recommend thorough review of the AI-suggested code before merging it into your project.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have something to add or modify.

## License

This project is licensed under the MIT license. For more information, refer to the [LICENSE](LICENSE) file.