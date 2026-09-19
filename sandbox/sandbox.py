def greet(*names, punctuation='!'):
    """Greet a list of names with a specified punctuation."""
    return "\n".join(f"hello {name}{punctuation}" for name in names)

print(greet("Ana", "Bo"))
