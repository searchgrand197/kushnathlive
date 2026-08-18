# CORS Configuration for Kushnath Ayurveda API

This document explains the CORS (Cross-Origin Resource Sharing) configuration for the Kushnath Ayurveda API to ensure proper communication between the frontend and backend.

## Current Configuration

### Allowed Origins
The API is configured to accept requests from the following origins:

- `https://kushnathayurveda.com` (Production)
- `https://www.kushnathayurveda.com` (Production with www)
- `http://localhost:5173` (Development - Vite)
- `http://127.0.0.1:5173` (Development - Vite)
- `http://localhost:5174` (Development - Vite alternative port)
- `http://127.0.0.1:5174` (Development - Vite alternative port)
- `http://localhost:8000` (Development - Django)
- `http://127.0.0.1:8000` (Development - Django)

### Allowed Methods
- GET
- POST
- PUT
- PATCH
- DELETE
- OPTIONS

### Allowed Headers
- accept
- accept-encoding
- authorization
- content-type
- dnt
- origin
- user-agent
- x-csrftoken
- x-requested-with
- cache-control
- pragma
- expires
- x-forwarded-for
- x-forwarded-proto

### Exposed Headers
- content-type
- content-length
- content-disposition

## Settings Files

### Development Settings (`settings.py`)
- `CORS_ALLOW_ALL_ORIGINS = False` (for security)
- `CORS_ALLOW_CREDENTIALS = True`
- `CORS_PREFLIGHT_MAX_AGE = 86400` (24 hours)

### Production Settings (`settings_production.py`)
- Stricter security settings
- HTTPS enforcement
- Secure cookie settings
- HSTS headers

## Testing CORS

### Using the Test Endpoint
A test endpoint is available at `/api/cors-test/` to verify CORS configuration:

```bash
# Test with curl
curl -H "Origin: https://kushnathayurveda.com" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type, Authorization" \
     -X OPTIONS \
     http://localhost:8000/api/cors-test/
```

### Using the Test Script
Run the provided test script:

```bash
python test_cors.py
```

## Common CORS Issues and Solutions

### 1. Preflight Request Failing
**Issue**: OPTIONS request returns 404 or doesn't include proper CORS headers
**Solution**: Ensure `corsheaders.middleware.CorsMiddleware` is in `MIDDLEWARE` before `CommonMiddleware`

### 2. Credentials Not Working
**Issue**: Cookies or Authorization headers not being sent
**Solution**: Set `CORS_ALLOW_CREDENTIALS = True` and ensure frontend includes `credentials: 'include'`

### 3. Multiple Origins
**Issue**: Need to allow multiple origins
**Solution**: Add all required origins to `CORS_ALLOWED_ORIGINS`

### 4. Custom Headers
**Issue**: Custom headers being blocked
**Solution**: Add headers to `CORS_ALLOW_HEADERS`

## Deployment Considerations

### Development
- Use `settings.py` with development-friendly settings
- `DEBUG = True`
- Less restrictive CORS settings

### Production
- Use `settings_production.py` with strict security
- `DEBUG = False`
- HTTPS enforcement
- Secure cookie settings

### Environment Variables
For production, consider using environment variables:

```python
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
```

## Troubleshooting

### Check CORS Headers
Look for these headers in API responses:
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`
- `Access-Control-Allow-Credentials`

### Browser Developer Tools
1. Open Developer Tools (F12)
2. Go to Network tab
3. Look for failed requests (red)
4. Check the CORS error details

### Common Error Messages
- `Access to fetch at '...' from origin '...' has been blocked by CORS policy`
- `No 'Access-Control-Allow-Origin' header is present on the requested resource`

## Security Notes

1. **Never use `CORS_ALLOW_ALL_ORIGINS = True` in production**
2. **Always specify exact origins in `CORS_ALLOWED_ORIGINS`**
3. **Use HTTPS in production**
4. **Set appropriate `CORS_PREFLIGHT_MAX_AGE` to reduce preflight requests**
5. **Monitor CORS errors in production logs**

## Additional Resources

- [Django CORS Headers Documentation](https://github.com/adamchainz/django-cors-headers)
- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [CORS Browser Support](https://caniuse.com/cors)
