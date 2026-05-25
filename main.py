from python_recipes import lazy_modules

lazy_modules.json.loads("")

print(lazy_modules.json.loads("{}"))
print(lazy_modules.sys.version)
session = lazy_modules.requests.Session()
