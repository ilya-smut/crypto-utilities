from flask import Flask, render_template, request, redirect
from pathlib import Path
import utilities

# Compute the directory of the current file
app_dir = Path(__file__).resolve().parent

# Set the absolute paths for templates and static folders
template_dir = Path(app_dir) / "templates"
static_dir = Path(app_dir) / "static"

# Initialize the application and its state
app = Flask("crypto-utils", template_folder=template_dir, static_folder=static_dir)


@app.route("/")
def root() -> str:
    return render_template("root.html")


@app.route("/gcd_route", methods=["POST"])
def gcd_route() -> str:
    gcd_a, gcd_b = int(request.form.get("a")), int(request.form.get("b"))
    if gcd_a and gcd_b:
        response_data = {'kind': 'gcd', 'text': f'Greatest Common Divisor of {gcd_a} and {gcd_b} is {str(utilities.get_gcd(gcd_a, gcd_b))}'}
        return render_template("root.html", results=response_data)
    else:
        return redirect("/")


@app.route("/ext_euclid_route", methods=["POST"])
def ext_euclid_route() -> str:
    a, b = int(request.form.get("a")), int(request.form.get("b"))
    if a and b:
        gcd, x, y = utilities.get_extended_euclid(a,b)
        text = f"{a}×{x} + {b}×{y} ≅ {gcd}"
        response_data = {'kind': 'ext_euclid', 'text': text}
        return render_template("root.html", results=response_data)
    else:
        return redirect("/")


@app.route("/amodp_route", methods=["POST"])
def amodp_route() -> str:
    a, p = int(request.form.get("a")), int(request.form.get("p"))
    if a and p:
        result = utilities.a_mod_p(a,p)
        text = f"{a} ≅ {result} mod {p}"
        response_data = {'kind': 'amodp', 'text': text}
        return render_template("root.html", results=response_data)
    else:
        return redirect("/")


@app.route("/modinv_route", methods=["POST"])
def modinv_route() -> str:
    a, p = int(request.form.get("a")), int(request.form.get("p"))
    if a and p:
        result = utilities.get_mod_inverse_fermat(a,p)
        text = f"inverse of {a} is {result} mod {p} "
        response_data = {'kind': 'modinv', 'text': text}
        return render_template("root.html", results=response_data)
    else:
        return redirect("/")


@app.route("/fastpow_route", methods=["POST"])
def fastpow_route() -> str:
    g, x, p = int(request.form.get("g")), int(request.form.get("x")), int(request.form.get("p"))
    if g and x and p:
        result = utilities.fast_powering(g,x,p)
        text = f"{g}^({x}) mod {p} ≅ {result}"
        response_data = {'kind': 'fastpow', 'text': text}
        return render_template("root.html", results=response_data)
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)