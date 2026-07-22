# Contributing to LiveMagic Pro

## 🤝 How to Contribute

We welcome contributions! Whether it's bug reports, feature requests, or code improvements.

### Types of Contributions

1. **Bug Reports** - Found an issue? Report it!
2. **Feature Requests** - Have an idea? Share it!
3. **Code Improvements** - Want to code? Submit a PR!
4. **Documentation** - Improve docs or translations?
5. **Testing** - Help test on different systems?

---

## 🐛 Bug Reports

### Before Reporting
1. Check existing issues: https://github.com/designshop39-jpg/LiveMagic-Pro/issues
2. Update to latest version
3. Check troubleshooting guide
4. Gather system information

### How to Report

1. Click "Issues" → "New Issue"
2. Choose "Bug report" template
3. Fill in details:
   - **Title**: Clear, concise description
   - **Description**: What happened?
   - **Steps to Reproduce**: How to replicate?
   - **Expected**: What should happen?
   - **Actual**: What actually happened?
   - **System Info**: OS, Python version, FFmpeg version
   - **Logs**: Include error messages and logs

### Example

```markdown
## Bug: Stream stops after 5 minutes

### Steps to Reproduce
1. Add video to playlist
2. Click START
3. Wait 5 minutes

### Expected
Stream should continue indefinitely

### Actual
Stream stops with "Connection reset" error

### System Info
- OS: Windows 11
- Python: 3.11.2
- FFmpeg: 6.0
- Error: See logs/channel_1.log

### Logs
```
[FFmpeg error output here]
```
```

---

## 💡 Feature Requests

### Before Requesting
1. Check if already requested
2. Check roadmap in README.md
3. Ensure it aligns with project scope

### How to Request

1. Click "Issues" → "New Issue"
2. Choose "Feature request" template
3. Describe:
   - **Feature**: What do you want?
   - **Problem**: What problem does it solve?
   - **Solution**: How should it work?
   - **Alternatives**: Other approaches?
   - **Use Cases**: When would you use it?

### Example

```markdown
## Feature: Dark/Light theme toggle

### Problem
Some users find dark mode too dark, want light theme option

### Solution
Add theme toggle in Settings menu with persistent storage

### Use Cases
- Streaming during daytime (light theme better)
- Accessibility (easier on eyes)
- Preference variation
```

---

## 💻 Code Contributions

### Setup Development Environment

1. **Fork Repository**
   ```bash
   # Go to https://github.com/designshop39-jpg/LiveMagic-Pro
   # Click "Fork"
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LiveMagic-Pro.git
   cd LiveMagic-Pro
   ```

3. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/issue-description
   ```

4. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Make Changes**
   - Follow code style guidelines
   - Add comments for complex logic
   - Test thoroughly

6. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add descriptive message"
   ```

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create Pull Request**
   - Go to original repo
   - Click "Compare & Pull Request"
   - Describe changes
   - Submit!

---

## 📝 Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Build, dependencies

### Examples

```bash
# Feature
git commit -m "feat(streaming): add scene transitions"

# Bug fix
git commit -m "fix(ui): resolve playlist scrollbar issue"

# Documentation
git commit -m "docs: add GPU encoding guide"

# Detailed commit
git commit -m "feat(encoder): add H.265 support

- Add libx265 codec option
- Update encoder presets
- Test on 4K video

Closes #123"
```

---

## 🧪 Testing

### Before Submitting PR

1. **Functionality**
   - Test your changes work
   - Test edge cases
   - Test error handling

2. **Compatibility**
   - Test on Windows/Mac/Linux if possible
   - Test with Python 3.9+
   - Test with different FFmpeg versions

3. **Code Quality**
   - Follow code style
   - No syntax errors
   - No debug print statements
   - Add comments where needed

4. **Documentation**
   - Update README if needed
   - Add docstrings
   - Update API.md if adding functions

### Testing Checklist

```markdown
- [ ] Code tested locally
- [ ] No syntax errors
- [ ] Follows code style
- [ ] Has docstrings
- [ ] Has comments where needed
- [ ] Updated documentation
- [ ] No debug code left
- [ ] Tested on multiple OSes (if applicable)
```

---

## 📋 Pull Request Process

### Before Submitting

1. Sync with main branch
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. Test thoroughly
3. Check code quality
4. Update documentation

### PR Template

```markdown
## Description
Briefly describe your changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes #(issue number)

## How to Test
Step-by-step testing instructions

## Checklist
- [ ] Code tested
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Follows code style

## Screenshots
Add screenshots if UI changed
```

---

## 🎨 Code Style Guidelines

### Python Style (PEP 8)

```python
# Good
def get_duration(path: str) -> float:
    """Get video duration in seconds."""
    try:
        output = subprocess.check_output([...])
        return float(output.strip())
    except Exception:
        return 0.0

# Bad
def getDuration(path):
    try:
        out = subprocess.check_output([...])
        return float(out.strip())
    except:
        return 0
```

### Naming
```python
# Functions and variables: snake_case
def get_ffmpeg_path():
    video_duration = 0

# Classes: PascalCase
class EnhancedChannelPanel:
    pass

# Constants: UPPER_CASE
FFMPEG = "ffmpeg"
DEFAULT_BITRATE = 3000
```

### Formatting
```python
# Lines: max 88 characters
# Indentation: 4 spaces
# Imports: at top, grouped
import os
import sys
from datetime import datetime
from tkinter import tk

# Docstrings: for all public functions
def my_function():
    """Short description.
    
    Longer description if needed.
    """
    pass
```

---

## 📚 Documentation

### What to Document
- Public functions
- Complex logic
- Configuration options
- Usage examples

### Docstring Format

```python
def get_duration(path: str) -> float:
    """Get video duration using ffprobe.
    
    Args:
        path (str): Path to video file
    
    Returns:
        float: Duration in seconds (0.0 on error)
    
    Example:
        >>> duration = get_duration("video.mp4")
        >>> print(f"Duration: {fmt_time(duration)}")
    """
    ...
```

---

## 🚀 Areas for Contribution

### High Priority
- [ ] Web interface (Flask/React)
- [ ] Mobile app support
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Streaming presets for each platform

### Medium Priority
- [ ] Cloud synchronization
- [ ] Advanced video filters
- [ ] Audio mixing board
- [ ] OBS integration
- [ ] Discord bot integration

### Low Priority
- [ ] Custom themes
- [ ] Keyboard shortcuts customization
- [ ] Performance optimizations
- [ ] Code refactoring

---

## ❓ Questions?

- Check DEVELOPMENT.md
- Check API.md
- Check existing issues and discussions
- Create an issue with your question

---

## 💬 Community

- **Report Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Pull Requests**: Always welcome!
- **Feature Ideas**: Open an issue

---

## 📜 Code of Conduct

### Be Respectful
- Treat everyone with respect
- No harassment or discrimination
- Accept constructive criticism
- Help others learn

### Be Professional
- Use clear, constructive language
- Focus on code, not people
- Assume good intentions
- Collaborate openly

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! Your help makes LiveMagic Pro better! 🙌**
