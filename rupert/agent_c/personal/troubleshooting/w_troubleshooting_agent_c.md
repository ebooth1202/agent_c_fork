# Agent C Troubleshooting Guide

## Container Environment Issues

### Error when running `.\agentc up` command

**Problem:** Command fails or shows connection errors

**Error message may include:**
```
unable to get image 'nginx:alpine': error during connect: this error may indicate that the docker daemon is not running: Get "http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.51/images/nginx:alpine/json": open //./pipe/docker_engine: The system cannot find the file specified.
```

**Solution:**
1. **Verify Rancher Desktop is running**
   - Check your system tray for the Rancher Desktop icon
   - If not running, open Rancher Desktop
   - Wait for it to fully start (icon should be green/active)
   - Run the command again:
   ```powershell
   .\agentc up
   ```

---

## Development Environment Issues

*(Issues specific to native development setups will be added here)*
