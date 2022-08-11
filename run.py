from flask import Flask, render_template, send_from_directory, make_response, request
from os import listdir
from os.path import isfile, isdir, join, abspath

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/")
    def root():
        arg = request.args.get("p")
        if arg == None: arg = ""
        path = f"../{arg}"

        if isfile(path):
            filename = path.split("/")[-1]
            filepath = abspath(path[:-1*len(filename)])
            print(filepath, filename)
            return send_from_directory(filepath, filename)
        elif isdir(path):
            with open("template.html") as template:
                page = template.read()
                target_location = page.find("<h3>Location: </h3>") + 14
                page = f"{page[:target_location]}{path[2:]}{page[target_location:]}"

                target_location = page.find("<hr>") + 4
                if len(path.split("/")) > 1 and path.split("/")[-1] != "":
                    item = "/".join(arg.split("/")[:-1])
                    add_context = f"\n        <a href=\"/?p={item}\">..</a><br>"
                    page = f"{page[:target_location]}{add_context}{page[target_location:]}"
                    target_location += len(add_context)
                for item in listdir(path):
                    add_context = f"\n        <a href=\"/?p={arg}/{item}\">{item}</a><br>"
                    page = f"{page[:target_location]}{add_context}{page[target_location:]}"
                    target_location += len(add_context)
            return page
        else:
            with open("404.html") as template:
                page = template.read()
            return make_response(page, 404)

    app.run("0.0.0.0", port=5006, debug=True)