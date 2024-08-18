from unidecode import unidecode

# Original text with encoding issues
text = "Dieter VÃ¶ltzke, Hans-Peter Abicht\nDirect laser sintering of ironâ€“graphite powder mixture A. Simchi, H. Pohl"

# Convert the text
converted_text = unidecode(text)

print(converted_text)
