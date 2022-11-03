from flask import Flask, request, send_file, render_template, make_response, redirect, url_for

app = Flask(__name__)

from exampleapp import exampleapp_bp

app.register_blueprint(exampleapp_bp)


@app.route("/favicon.ico")
def favicon():
    try:
        return send_file('/path/to/project/image.ico', mimetype='image/vnd.microsoft.icon')
    except:
        return ''


@app.route("/")
def index():
    return render_template("index.html", **request.cookies)


@app.route('/search', methods=['POST'])
def search():
    searchdata = request.form['searchdata']

    sites = {
        'Index Page': {'tags': ['home', 'index', 'page'], 'route': 'index'},
        'Second Page': {'tags': ['second', 'page'], 'route': 'exampleapp_bp.second_page_index'},
        'Upload Files': {'tags': ['upload', 'file'], 'route': 'exampleapp_bp.second_page_upload'},
        'View Files': {'tags': ['view', 'file'], 'route': 'exampleapp_bp.second_page_files'}
    }

    results = {}

    for site in sites:
        for tag in sites[site]['tags']:
            if tag in searchdata.lower():
                results[site] = {'route': sites[site]['route']}

    if len(results) > 1:
        out = ""
        for result in results:
            out += "<p><a href='{}'>{}</a></p>".format(url_for(results[result]['route']), result)
        return render_template("search.html", searchdata=searchdata, listofresults=out)
    else:
        for result in results:
            return redirect(url_for(results[result]['route']))
    return redirect(url_for('index'))


@app.route("/clearcookie", defaults={'cookie': None})
@app.route("/clearcookie/<cookie>")
def base_clearcookie(cookie):
    res = make_response(redirect(url_for("index")))
    res.set_cookie(cookie, "false", max_age=2629800)
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0')
