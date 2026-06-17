# Module 18 — Security for Android Apps

> Protect user data, secrets, and APIs — mapped to the OWASP Mobile Top 10.

**Status:** ✅ **Fully written**
**Prerequisites:** [Module 13 — Architecture](../module-13-architecture/README.md).
**Level:** 🟡🔴 · **Est.:** 5–7 hrs

## What you'll be able to do
- Store secrets and tokens safely with Keystore-backed encryption.
- Harden API communication.
- Audit an app against the OWASP Mobile Top 10.

## Lessons
| # | Lesson | You'll learn |
|---|---|---|
| 01 | [The Android security model](01-android-security-model.md) | sandboxing, permissions, the threat model. |
| 02 | [Secure storage](02-secure-storage.md) | Keystore, encrypted DataStore, what *not* to store. |
| 03 | [Encryption](03-encryption.md) | symmetric/asymmetric basics; key management. |
| 04 | [API security](04-api-security.md) | TLS, certificate pinning, token handling. |
| 05 | [Authentication & authorization](05-authentication-authorization.md) | sessions, OAuth, biometric gating. |
| 06 | [OWASP Mobile Top 10](06-owasp-mobile-top-10.md) | each risk with an Android-specific mitigation. |

## Interview focus
Where to store a refresh token; certificate pinning trade-offs; an OWASP risk + mitigation.

## AI assistant focus
Using AI to threat-model a feature; reviewing for hardcoded secrets and insecure storage — never trusting it blindly on crypto.
