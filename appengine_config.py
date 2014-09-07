from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    app = SessionMiddleware(app, cookie_key="jhdsohdehgosdh3489vgosdhbvgohsdbvohosdhbvosdhbvoisdhbbusdvfioasdbvobdaviob")
    return app