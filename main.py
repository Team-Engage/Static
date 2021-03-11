from jinja2 import Environment, FileSystemLoader, select_autoescape
from glob import glob
import os
import subprocess


env = Environment(
  loader=FileSystemLoader("templates"),
  autoescape=select_autoescape(["html", "xml"])
)

templates_list = [
  "index.html"
]


# Removes all files in site folder
def clear_site_folder():
  subprocess.run(["rm", "-r", "site"])
  subprocess.run(["mkdir", "site"])


def build_site():
  clear_site_folder()

  # Builds templates
  for i in templates_list:
    tmp = env.get_template(i)

    with open(f"site/{i}", "wt") as f:
      f.write(tmp.render())
  
  # Adds static files
  os.mkdir("site/static")
  for i in glob("static/*"):
    with open(i, "rb") as og_file:
      with open(f"site/static/{os.path.basename(i)}", "wb") as new_file:
        new_file.write(og_file.read())


def run(build=True):
  if build:
    build_site()

  subprocess.run(["python", "-m", "http.server", "8000", "--directory", "site"])


if __name__ == "__main__":
  run(build=True)
