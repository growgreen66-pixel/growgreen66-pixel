# File permissions notes and examples

This short file documents common file permission commands and secure defaults you can use on Linux systems. It's intended as a learning artifact for coursework and interviews.

Basic concepts
- Owner (u), Group (g), Others (o)
- Read (r), Write (w), Execute (x)
- Numeric (octal) and symbolic modes (e.g., 644, u=rw,g=r,o=r)

Examples
- Make a file readable/writable by owner, readable by group/others:
  chmod 644 sample.txt

- Make a script executable by owner only:
  chmod 700 run_analysis.sh

- Set ownership to user:group:
  chown alice:security sample.txt

- Recursively set directory and file permissions (safe pattern):
  find /path/to/dir -type d -exec chmod 750 {} +
  find /path/to/dir -type f -exec chmod 640 {} +

- Create files with a restrictive default umask (e.g., 027):
  # set for current shell
  umask 027
  # this makes new files created as 640 and new dirs as 750 by common tools

Best practices
- Minimize use of 777; prefer least privilege.
- Use groups to share access rather than granting broad "others" permissions.
- For web-facing files, ensure files are not world-writable and execute permissions are limited to what is required.
- Consider using setfacl for fine-grained ACLs if needed.

This document is a short example to show understanding of Linux permissions and secure defaults. It can be expanded with examples from lab exercises if you want.
