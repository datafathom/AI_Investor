
try:
    print("Importing attribution_api...")
    from web.api.attribution_api import attribution_bp
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
