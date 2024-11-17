# Remove common patterns
remove_patterns = [
    r'\d{2,4}p .*|19\d{2}|20\d{2}',
    r'BluRay|HDTV|WebRip|HDRip|WEBDL|WEB_DL|HD|DVD',
    r'x264|x265|AAC|MP3|AAC2|HEVC',
    r'RARBG|YIFY|TamilRockers|Einthusan|www\.TamilRockers\.net',
    r'\[.*?\]|\(.*?\) .*$',
    r'Malayalam|Tamil|Telugu',
    r'in HD .*$|Prope',
    r'\.mkv|\.mp4|\.avi',
    r'New|ORG|1CD|HC|MM'
]

# Replace patterns with spaces
replace_patterns = [
    r'\s+',
    r'[^a-zA-Z0-9\s]',
    r'_+'
]