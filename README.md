# InkHour

A Python-based digital clock that displays the current time through literary quotes. InkHour combines the timeless appeal of literature with modern e-ink technology (Papirus) to show time-related quotes from literature that match the current time, creating a unique intersection of classic storytelling and contemporary timekeeping.

## Overview

The Literary Clock pulls quotes from a JSON database and displays them on an e-ink screen, with special formatting for time references within the quotes. When the current time matches a time mentioned in literature, the display updates to show the relevant quote along with its source.

## Features

- Displays literary quotes containing references to the current time
- Dynamically formats quotes with emphasized time references
- Rotatable display support
- Configurable font sizes and text formatting
- Quote filtering based on length
- Attribution display for books and authors
- Automatic display updates every 30 seconds

## Requirements

- Python 3.x
- Papirus e-ink display
- Required Python packages:
  - `papirus`
  - Additional standard libraries: `datetime`, `json`, `os`, `random`, `time`

## Configuration

The following parameters can be adjusted in the code:

```python
dispWidth = 200          # Display width in pixels
screenRot = 0           # Screen rotation in degrees
typeSize = 12           # Base font size
quoteLen = 70          # Maximum quote length
timeSizeIncrease = 1    # Time text size increase
sourceSizeDecrease = 1  # Source text size decrease
lineSpacing = 1.2       # Line spacing multiplier
maxQuoteLen = 250      # Maximum quote length in characters
```

## Data Format

The project expects quotes to be stored in a `quotes.json` file with the following structure:

```json
{
    "HH:MM": [
        {
            "quote": "Quote text containing the time",
            "book": "Book Title",
            "author": "Author Name",
            "timeAlt": "Alternative time format (optional)"
        }
    ]
}
```

## Usage

1. Ensure all requirements are installed
2. Place your `quotes.json` file in the same directory as the script
3. Run the script:

```bash
python literary_clock.py
```

The program will:
1. Load and filter quotes from the JSON file
2. Initialize the e-ink display
3. Continuously update the display with quotes matching the current time
4. Handle display formatting and rotation automatically

## Error Handling

The script includes robust error handling for:
- Missing or invalid JSON file
- Display update failures
- Quote formatting issues
- General runtime exceptions

## Display Layout

The display format follows this structure:
1. Quote prefix (if time appears mid-quote)
2. Time reference (enlarged)
3. Quote suffix (if any)
4. Source attribution (slightly smaller text)

## Contributing

Feel free to contribute to this project by:
- Adding new quotes to the database
- Improving the display formatting
- Optimizing the refresh rate
- Adding new features

## License

[Add your chosen license here]

## Acknowledgments

- Built using the Papirus e-ink display library
- Inspired by literary timepieces and book lovers everywhere