import csv
from io import StringIO

def generate_csv(comments, video_title, channel_name):
    output = StringIO()
    writer = csv.writer(output)

    # First row: Video Title and Channel Name
    writer.writerow([f"Video Title: {video_title}", f"Channel Name: {channel_name}"])
    writer.writerow([])  # Empty row
    
    # Third row: Headers
    writer.writerow(["Username", "Comment"])

    # Add comments
    for comment in comments:
        writer.writerow([comment["author-text"], comment["content-text"]])
    
    output.seek(0)
    return output.getvalue()