import io
import contextlib
import traceback


def run_python_code(code: str):
    output = io.StringIO()

    try:
        safe_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "sorted": sorted,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
            }
        }

        with contextlib.redirect_stdout(output):
            exec(code, safe_globals)

        result = output.getvalue().strip()

        if result:
            return result

        return "Code executed successfully."

    except Exception:
        return traceback.format_exc()
