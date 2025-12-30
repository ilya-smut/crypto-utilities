from flask import Flask, render_template, request, redirect, session
from pathlib import Path
import utilities
from state import SavedValues, ResponseData

# Compute the directory of the current file
app_dir = Path(__file__).resolve().parent

# Set the absolute paths for templates and static folders
template_dir = Path(app_dir) / "templates"
static_dir = Path(app_dir) / "static"

# Initialize the application and its state
app = Flask("crypto-utils", template_folder=template_dir, static_folder=static_dir)

saved_values = SavedValues()

def prepare_response(response_data: ResponseData = None, append_saved = True, replace_saved=False, set_combo_op=True):
    if not response_data:
        response_data = ResponseData()
    if append_saved:
        response_data.add_saved_value(saved_values.get_saved_pairs(), replace=replace_saved)
    if set_combo_op:
        op = request.form.get("combo_op") or "gcd"
        response_data.set_combo_op(op)
    return response_data

@app.route("/")
def root() -> str:
    response_data = prepare_response()
    return render_template("root.html.j2", response=response_data.values())


@app.route("/gcd_route", methods=["POST"])
def gcd_route() -> str:
    response_data = prepare_response()
    a_raw = request.form.get("a")
    b_raw = request.form.get("b")
    if not a_raw or not b_raw:
        return render_template("root.html.j2", response=response_data.values())
    a = int(a_raw); b = int(b_raw)
    kind = "combo"
    response_data.add_result({'kind': kind, 'text': f'Greatest Common Divisor of {a} and {b} is {str(utilities.get_gcd(a, b))}'})
    print(response_data.values())
    return render_template("root.html.j2", response=response_data.values())


@app.route("/ext_euclid_route", methods=["POST"])
def ext_euclid_route() -> str:
    response_data = prepare_response()
    a, b = int(request.form.get("a")), int(request.form.get("b"))
    if a and b:
        gcd, x, y = utilities.get_extended_euclid(a,b)
        text = f"{a}×{x} + {b}x{y} = {gcd}"
        kind = "combo"
        response_data.add_result({'kind': kind, 'text': text})
        return render_template("root.html.j2", response=response_data.values())
    else:
        return redirect("/")


@app.route("/amodp_route", methods=["POST"])
def amodp_route() -> str:
    response_data = prepare_response()
    a, p = int(request.form.get("a")), int(request.form.get("p"))
    if a and p:
        result = utilities.a_mod_p(a,p)
        text = f"{a} ≅ {result} mod {p}"
        kind = "combo"
        response_data.add_result({'kind': kind, 'text': text})
        return render_template("root.html.j2", response=response_data.values())
    else:
        return redirect("/")


@app.route("/modinv_route", methods=["POST"])
def modinv_route() -> str:
    a, p = int(request.form.get("a")), int(request.form.get("p"))
    response_data = prepare_response()
    if a and p:
        result = utilities.get_mod_inverse_euclid(a,p)  # Fermat will work only with prime modulus
        text = f"inverse of {a} is {result} mod {p} "
        kind = "combo"
        response_data.add_result({'kind': kind, 'text': text})
        return render_template("root.html.j2", response=response_data.values())
    else:
        return redirect("/")


@app.route("/fastpow_route", methods=["POST"])
def fastpow_route() -> str:
    g, x, p = int(request.form.get("g")), int(request.form.get("x")), int(request.form.get("p"))
    response_data = prepare_response()
    if g and x and p:
        result = utilities.fast_powering(g,x,p)
        text = f"{g}^({x}) mod {p} ≅ {result}"
        kind = "combo"
        response_data.add_result({'kind': kind, 'text': text})
    return render_template("root.html.j2", response=response_data.values())

@app.route("/save_value", methods=["POST"])
def save_value() -> str:
    name, value = request.form.get("name"), request.form.get("value")
    response_data = prepare_response()
    if name and value:
        saved_values.add_value(name, value)
        response_data = prepare_response(response_data)
    return render_template("root.html.j2", response=response_data.values())

@app.route("/delete_value", methods=["POST"])
def delete_value() -> str:
    name = request.form.get("name")
    response_data = prepare_response()
    if name:
        saved_values.remove_saved(name)
        response_data = prepare_response(response_data, replace_saved=True)
    return render_template("root.html.j2", response=response_data.values())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)