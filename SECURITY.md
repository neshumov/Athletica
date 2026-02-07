# Security Policy

This repository is public. No plaintext secrets are allowed.

## Secrets Management (SOPS)

All sensitive configuration must be stored in SOPS-encrypted files:

- `secrets.dev.enc.yaml`
- `secrets.prod.enc.yaml`

Plaintext `.env` files are forbidden.

### Generate Age Key

1. Install `age` and `sops`.
2. Create a key:

```bash
age-keygen -o ~/.config/sops/age/keys.txt
```

3. Export the public key for SOPS:

```bash
age-keygen -y ~/.config/sops/age/keys.txt
```

### Encrypt Secrets

```bash
sops --encrypt --age <PUBLIC_KEY> secrets.dev.yaml > secrets.dev.enc.yaml
```

### Decrypt Locally

```bash
sops --decrypt secrets.dev.enc.yaml > secrets.dev.dec.yaml
```

### Runtime Injection

Use decrypted values at runtime via env vars:

```bash
export $(sops -d secrets.dev.enc.yaml | yq -r 'to_entries|map("ATHLETICA_" + (.key|ascii_upcase) + "=" + (.value|tostring))|.[]')
```

### Rotation

- Create a new age key.
- Re-encrypt the secrets with the new key.
- Revoke the old key.

## Reporting

If you discover a security issue, open a private disclosure to the repository owner.
