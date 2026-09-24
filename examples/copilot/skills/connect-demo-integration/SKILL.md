---
name: connect-demo-integration
description: Connects a real service to the demo to replace a simulated source.
---

# Connect a service

Ask which service to connect and which operation to demonstrate.

1. Read the HLD and existing code; reuse the data contract.
2. Check the API and prerequisites in the official documentation.
3. Add the connection without writing secrets in code or logs.
4. Test a simple call, then the error behavior.
5. Document the configuration and what was actually verified.

Keep an explicit simulated mode, without an automatic fallback that hides a failure.
Ask for confirmation before any write operation or external action.
Do not blindly retry an action that could create a duplicate.
If access is missing, report the blocker instead of inventing a result.
