# Create Cert

**Script:** [Create Cert (script)](../create_cert.py)

## Purpose
One-time self-signed code-signing certificate generator. Run once
(`python setup/create_cert.py`); refuses to overwrite an existing
`setup/cert/UltraVivid.pfx`. Reads the password from
`setup/cert/password.txt` (create manually first — never hardcoded, root
Rule #4) and writes the `.pfx` via PowerShell's `New-SelfSignedCertificate`
+ `Export-PfxCertificate` (`CN=UVuruna`, `CodeSigningCert`, 5-year validity).

`setup/cert/` is gitignored — the `.pfx` and `password.txt` are never
committed; back them up externally.

## Connections

### Used by
- The owner, manually, once — [Build](build.md) reads the `.pfx` it produces
