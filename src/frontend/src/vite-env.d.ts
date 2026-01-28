/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_APP_NAME: string;
  readonly VITE_APP_ENV: string;
  readonly VITE_APP_VERSION: string;
  readonly VITE_APP_DEBUG: string;
  readonly VITE_FEATURE_SUBSCRIPTIONS: string;
  readonly VITE_FEATURE_PAYMENTS: string;
  readonly VITE_FEATURE_SOLANA: string;
  readonly VITE_FEATURE_SIGNALS: string;
  readonly VITE_SECURE_COOKIES: string;
  readonly VITE_CSRF_PROTECTION: string;
  readonly VITE_BUNDLE_ANALYZE: string;
  readonly VITE_SOURCE_MAP: string;
  readonly VITE_SENTRY_DSN: string;
  readonly VITE_GOOGLE_ANALYTICS_ID: string;
  readonly VITE_DEFAULT_LOCALE: string;
  readonly VITE_SUPPORTED_LOCALES: string;
  readonly VITE_STORAGE_PREFIX: string;
  readonly VITE_SESSION_TIMEOUT: string;
  readonly VITE_API_TIMEOUT: string;
  readonly VITE_POLLING_INTERVAL: string;
  readonly VITE_CACHE_DURATION: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
