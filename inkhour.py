from papirus import PapirusTextPos # Requires installation of PaPiRus libararies
import datetime
import json
import os
import random
import time

# Configuration variables
dispWidth = 200     # Display width in Pixels
screenRot = 0       # Screen rotation in degrees, 0 corrseponds to the USB ports facing up on the Pi Zero
baseTypeSize = 12   # Base font size in pts
quoteLen = 70       # Maximum quote length in chars
timeSizeInc = 1     # How much bigger the time text should be starting from baseTypeSize
sourceSizeDec = 1   # How much smaller the source text should be starting from baseTypeSize
lineSpacing = 1.2   # Space between lines as a multiplier of font size
maxQuoteLen = 250   # Max number of chars allowed in the quote
showAuthor = False  # Choose to display the authors name after the book title, best for larger screens

def load_quotes():
    """Load quotes from quotes.json file"""
    try:
        with open('quotes.json', 'r') as file:
            raw_quotes = json.load(file)
            
        # Filter quotes to only include those under 60 characters
        quotes = {}
        total_quotes = 0
        filtered_quotes = 0
        
        for time, quote_list in raw_quotes.items():
            quotes[time] = []
            for quote in quote_list:
                total_quotes += 1
                if len(quote['quote']) <= maxQuoteLen:
                    quotes[time].append(quote)
                else:
                    filtered_quotes += 1
            
            # Remove time slots with no valid quotes
            if not quotes[time]:
                del quotes[time]
        
        print(f"Loaded {total_quotes - filtered_quotes} quotes for {len(quotes)} different times")
        print(f"Filtered out {filtered_quotes} quotes that were too long")
        return quotes
    except FileNotFoundError:
        print("Error: quotes.json not found")
        return {}
    except json.JSONDecodeError:
        print("Error: quotes.json is not valid JSON")
        return {}
    except Exception as e:
        print(f"Error loading quotes: {e}")
        return {}

def calculate_text_height(text, font_size):
    ##Calculate approximate height needed for text at given font size
    #Approximate pixels per character (varies by font)
    #For monospace fonts, width is roughly equal to height
    pixels_per_char = font_size * 0.6  # This is approximate
    
    # Calculate the number of chars that fit on one line
    chars_per_line = int(dispWidth / pixels_per_char)

    #Adjusts based on your display width and font size
    num_lines = (len(text) + chars_per_line - 1) // chars_per_line
    
    return num_lines * (font_size * lineSpacing)

def update_display(display, quote_data, current_time):
    """Update the e-ink display"""
    try:
        quote = quote_data['quote']
        book = quote_data.get('book', 'Unknown')
        author = quote_data.get('author', '')
        time_alt = quote_data.get('timeAlt', current_time)

        # Clear previous content
        display.Clear()
        
        y_pos = 3  # Starting Y position
        
        # If there's a time reference, split and display with different sizes
        if time_alt in quote:
            parts = quote.split(time_alt)
            
            # Ensure quote isn't too long
            if len(quote) > quoteLen:
                parts[1] = parts[1][:quoteLen - len(parts[0]) - len(time_alt) - 3] + "..."
            
            # Display first part
            if parts[0]:
                display.AddText(parts[0], 5, y_pos, size=baseTypeSize, Id="prefix")
                y_pos += calculate_text_height(parts[0], baseTypeSize)

            # Display time in larger font
            display.AddText(time_alt, 5, y_pos, size=baseTypeSize + timeSizeIncrease, Id="time")
            y_pos += calculate_text_height(time_alt, baseTypeSize + timeSizeIncrease)

            # Display remainder of quote
            if parts[1]:
                display.AddText(parts[1], 5, y_pos, size=baseTypeSize, Id="suffix")
                y_pos += calculate_text_height(parts[1], baseTypeSize)
            
        else:
            # Display full quote if no time reference found
            if len(quote) > quoteLen:
                quote = quote[:quoteLen - 3] + "..."
            display.AddText(quote, 5, y_pos, size=baseTypeSize, Id="quote")
            y_pos += calculate_text_height(quote, baseTypeSize)

        # Add source attribution with some extra spacing
        source = f"- {book}"
        
        if showAuthor:
            if author:
                source += f" ({author})"
        
        #print(y_pos)
        y_pos += -2  # Add extra space before source
        display.AddText(source, 5, y_pos, size=baseTypeSize - sourceSizeDecrease, Id="source")
        display.WriteAll() #Push everything to the display

        return True
    except Exception as e:
        print(f"Error updating display: {e}")
        return False

def main():
    quotes = load_quotes()
    if not quotes:
        print("No quotes loaded, exiting...")
        return

    # Initialize display with rotation
    # Set autoUpdate to false to allow us to push all the content to the screen at once
    display = PapirusTextPos(False, rotation=screenRot)
    
    last_time = ""
    print("Literary Clock starting...")
    
    while True:
        try:
            current_time = datetime.datetime.now().strftime("%H:%M")
            
            # Only update if minute has changed
            if current_time != last_time:
                print(f"Time changed to {current_time}")
                if current_time in quotes:
                    quote = random.choice(quotes[current_time])
                    if update_display(display, quote, current_time):
                        print(f"Updated display with quote from {quote['book']}")
                    else:
                        print("Failed to update display")
                else:
                    print(f"No quote available for {current_time}")
                last_time = current_time
                
            # Sleep for 30 seconds before checking again
            time.sleep(30)

        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(30)  # Keep going even if there's an error

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")