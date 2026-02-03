
try:
    print("Importing dashboard_api...")
    from web.api.dashboard_api import dashboard_bp
    print("Importing attribution_api...")
    from web.api.attribution_api import attribution_bp
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
