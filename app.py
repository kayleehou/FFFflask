import json 
from jinja2 import Environment, FileSystemLoader

with open("dogs.json", "r") as d:
    dogs = json.load(d)
    
fileLoader = FileSystemLoader("templates")
env = Environment(loader=fileLoader)

rendered = env.get_template("stub.html").render(dogs=dogs, title="Dogs")

# Write HTML to a file - page.html

fileName = "page.html"

with open(f"./site/{fileName}", "w") as f:
    f.write(rendered)
