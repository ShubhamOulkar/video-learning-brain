> [!IMPORTANT]
> **Note for contributors:** When branching out, create a new branch from the `dev` branch.

# 🎉 Welcome to **cognee**!

We're excited that you're interested in contributing to our project!
We want to ensure that every user and contributor feels welcome, included and supported to participate in cognee community.
This guide will help you get started and ensure your contributions can be efficiently integrated into the project.

## 🌟 Quick Links

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Discord Community](https://discord.gg/bcy8xFAtfd)
- [Issue Tracker](https://github.com/topoteretes/cognee/issues)
- [Cognee Docs](https://docs.cognee.ai)

## 1. 🚀 Ways to Contribute

You can contribute to **cognee** in many ways:

- 📝 Submitting bug reports or feature requests
- 💡 Improving documentation
- 🔍 Reviewing pull requests
- 🛠️ Contributing code or tests
- 🌐 Helping other users

## 📫 Get in Touch

There are several ways to connect with the **cognee** team and community:

### GitHub Collaboration
- [Open an issue](https://github.com/topoteretes/cognee/issues) for bug reports, feature requests, or discussions
- Submit pull requests to contribute code or documentation
- Join ongoing discussions in existing issues and PRs

### Community Channels
- Join our [Discord community](https://discord.gg/bcy8xFAtfd) for real-time discussions
- Participate in community events and discussions
- Get help from other community members

### Direct Contact
- Email: vasilije@cognee.ai
- For business inquiries or sensitive matters, please reach out via email
- For general questions, prefer public channels like GitHub issues or Discord

We aim to respond to all communications within 2 business days. For faster responses, consider using our Discord channel where the whole community can help!

## Issue Labels

To help you find the most appropriate issues to work on, we use the following labels:

- `good first issue` - Perfect for newcomers to the project
- `bug` - Something isn't working as expected
- `documentation` - Improvements or additions to documentation
- `enhancement` - New features or improvements
- `help wanted` - Extra attention or assistance needed
- `question` - Further information is requested
- `wontfix` - This will not be worked on


## 2. 🛠️ Development Setup

### Required tools
* [Python](https://www.python.org/downloads/)
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* pre-commit: `uv run pip install pre-commit && pre-commit install`

### Fork and Clone

1. Fork the **cognee** repository
2. Clone your fork:
```shell
git clone https://github.com/<your-github-username>/cognee.git
cd cognee
```
### Create a Branch

Create a new branch for your work:
```shell
git checkout -b feature/your-feature-name
```

## 3. 🎯 Making Changes

1. **Code Style**: Follow the project's coding standards
2. **Documentation**: Update relevant documentation
3. **Tests**: Add tests for new features
4. **Commits**: Write clear commit messages

### Running Tests

Copy `.env.template` to `.env` and provide your OPENAI_API_KEY as LLM_API_KEY

```shell
uv run python cognee/tests/test_library.py
```

### Running Simple Example

Copy `.env.template` to `.env` and provide your OPENAI_API_KEY as LLM_API_KEY

Make sure to run ```shell uv sync ``` in the root cloned folder or set up a virtual environment to run cognee

📤 Submitting Changes

1. Make sure that `pre-commit` and hooks are installed. See `Required tools` section for more information. Try executing `pre-commit run` if you are not sure.
3. Push your changes:
```shell
git add .
git commit -s -m "Description of your changes"
git push origin feature/your-feature-name
```

Thank you for contributing to **cognee**! 🌟
