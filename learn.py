import requests
import json
from jinja2 import Template, Environment, FileSystemLoader

# Define the URL patterns for the JSON files
json_urls = [
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/1",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/2",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/3",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/4",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/5",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/6",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/7",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/8",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/9",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/10",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/11",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/12",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/13",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/14",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/15",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/16",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/17",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/18",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/19",
    "https://fluffyfriendfinder.nighthawkcodingsociety.com/api/users/20",
]

# Load the Jinja template from a file
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('templates/learn.html')


# Loop over the JSON URLs and generate a table for each one
for url in json_urls:
    # Fetch the data from the JSON file
    response = requests.get(url)
    data = json.loads(response.text)

    # Process the data as needed
    # ...

    # Render the Jinja template with the processed data
    table_html = template.render(data=data)

    # Write the generated HTML to a file
    filename = url.split("/")[-1].replace(".json", ".html")
    with open(filename, "w") as f:
        f.write(table_html)

with open("templates/learn.html", "r") as f:
    template_text = f.read()
    template = Template(template_text)
    

# Render the template with the JSON URLs
table_html = template.render(json_urls=json_urls)