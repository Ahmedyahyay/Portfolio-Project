"""
Session interface override to fix TypeError with 'partitioned' cookie argument
Following copilot instructions for compatibility fixes
"""

from flask.sessions import SecureCookieSessionInterface
from flask import Flask

class FixedSessionInterface(SecureCookieSessionInterface):
    """Override session interface to handle 'partitioned' cookie argument error"""
    
    def save_session(self, app, session, response):
        """Override to remove 'partitioned' argument that causes TypeError"""
        try:
            # Get the original save_session method
            domain = self.get_cookie_domain(app)
            path = self.get_cookie_path(app)
            
            if not session:
                if session.modified:
                    # Remove session cookie by setting it to empty with past expiration
                    response.delete_cookie(
                        app.session_cookie_name,
                        domain=domain,
                        path=path,
                        secure=self.get_cookie_secure(app),
                        httponly=self.get_cookie_httponly(app),
                        samesite=self.get_cookie_samesite(app)
                        # Note: Removed 'partitioned' argument to fix TypeError
                    )
                return
            
            # If session has data, save it normally
            if self.should_set_cookie(app, session):
                httponly = self.get_cookie_httponly(app)
                secure = self.get_cookie_secure(app)
                expires = self.get_expiration_time(app, session)
                val = self.get_signing_serializer(app).dumps(dict(session))
                
                response.set_cookie(
                    app.session_cookie_name,
                    val,
                    expires=expires,
                    httponly=httponly,
                    domain=domain,
                    path=path,
                    secure=secure,
                    samesite=self.get_cookie_samesite(app)
                    # Note: Removed 'partitioned' argument to fix TypeError
                )
                
        except Exception as e:
            # Fallback to parent implementation without partitioned argument
            app.logger.warning(f"Session save error (using fallback): {e}")
            super().save_session(app, session, response)

def apply_session_fix(app: Flask):
    """Apply session interface fix to Flask app following copilot patterns"""
    app.session_interface = FixedSessionInterface()
    app.logger.info("✅ Applied session interface fix for 'partitioned' cookie error")
    return app
