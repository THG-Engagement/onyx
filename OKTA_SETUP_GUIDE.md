# Setting up Okta OIDC Authentication for Onyx

This guide will walk you through setting up OpenID Connect (OIDC) authentication with Okta for Onyx.

> **Note:** We've implemented OIDC support in the non-enterprise edition by modifying the authentication code. This allows you to use Okta OIDC authentication without requiring the enterprise edition.

## 1. Create an Okta Application

1. Log in to your Okta Admin Dashboard
2. Navigate to **Applications** > **Applications**
3. Click **Create App Integration**
4. Select **OIDC - OpenID Connect** as the sign-in method
5. Choose **Web Application** as the application type
6. Click **Next**

## 2. Configure the Okta Application

1. Name your application (e.g., "Onyx")
2. For **Sign-in redirect URIs**, enter: `http://localhost:3000/auth/oidc/callback` (adjust the domain if your Onyx instance is hosted elsewhere)
3. For **Sign-out redirect URIs**, enter: `http://localhost:3000` (adjust as needed)
4. Under **Assignments**, select either "Allow everyone in your organization to access" or "Limit access to selected groups" based on your requirements
5. Click **Save**

## 3. Get Your Okta Application Credentials

After creating the application, you'll be taken to the application's settings page. Note down the following:

- **Client ID**
- **Client Secret**
- Your **Okta domain** (e.g., `dev-123456.okta.com`)

## 4. Test Your Okta Configuration

Before configuring Onyx, you can verify your Okta OIDC configuration using the provided test script:

```bash
./test_okta_config.py
```

When prompted, enter your Okta domain. The script will check if the OpenID configuration URL is accessible and correctly formatted.

Alternatively, you can provide the URL directly:

```bash
./test_okta_config.py --url https://your-okta-domain/.well-known/openid-configuration
```

## 5. Configure Onyx for Okta OIDC

1. Open the `.env` file in the `deployment` directory
2. Update the following values with your Okta credentials:
   ```
   OAUTH_CLIENT_ID=your-okta-client-id
   OAUTH_CLIENT_SECRET=your-okta-client-secret
   OPENID_CONFIG_URL=https://your-okta-domain/.well-known/openid-configuration
   ```
3. Generate a secure random string for the SECRET value:
   ```bash
   openssl rand -hex 32
   ```
4. Update the SECRET value in the .env file with this generated string

## 5. Start Onyx with OIDC Authentication

1. Navigate to the deployment directory:
   ```bash
   cd deployment
   ```

2. Start Onyx using Docker Compose:
   ```bash
   docker-compose -f docker_compose/docker-compose.prod.yml up -d
   ```

## 6. Test the Integration

1. Navigate to your Onyx instance (e.g., `http://localhost:3000`)
2. You should be redirected to the Okta login page
3. After successful authentication, you'll be redirected back to Onyx

## Troubleshooting

- **Redirect URI Mismatch**: Ensure the redirect URI in your Okta application settings exactly matches the URI used by Onyx (`http://localhost:3000/auth/oidc/callback` by default)
- **Scopes**: By default, Onyx requests the standard OpenID scopes. If you need additional scopes, add the following to your .env file:
  ```
  OIDC_SCOPE_OVERRIDE=openid,email,profile,additional_scope
  ```
- **Logs**: Check the Onyx logs for any authentication-related errors:
  ```bash
  docker-compose -f docker_compose/docker-compose.prod.yml logs api_server