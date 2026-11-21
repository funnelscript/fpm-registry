# FunnelScript Official Package Registry

Official, zero-server package registry for the **FunnelScript** language, hosted on **GitHub Pages**.

## Structure
- `index/<scope>/<name>.json`: Static package metadata and version manifest.
- `tarballs/<scope>/<name>-<version>.tar.gz`: Content-addressed package archives.

## Automated Verification
Run offline verification of all registry packages and checksums:
```bash
python3 scripts/validate_registry.py
```
