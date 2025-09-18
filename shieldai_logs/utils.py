def load_log(file_path):
    """
    Carga un log de texto plano y devuelve sus líneas.
    Si ocurre un error, devuelve {"error": "..."}.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except Exception as e:
        return {"error": str(e)}
