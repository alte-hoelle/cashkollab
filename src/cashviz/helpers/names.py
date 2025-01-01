def clean_name(name: str) -> str:
    return (
        name.lower()
        .replace("ä", "ae")
        .replace("ü", "ue")
        .replace("ö", "oe")
        .replace("ß", "ss")
    )
