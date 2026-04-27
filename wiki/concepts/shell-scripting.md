---
title: "Shell Scripting"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [shell, bash, scripting, automation, linux, command-line]
---

## Overview

Shell scripting is the practice of writing sequences of commands for a Unix/Linux shell or command-line interpreter to execute. A shell script is a text file containing commands that would typically be entered interactively at a terminal prompt, combined with programming constructs like variables, conditionals, loops, and functions that enable complex automation and logic.

Shell scripting predates modern programming languages—Unix shells like sh (Bourne shell) and csh emerged in the 1970s alongside the development of Unix operating systems. Despite decades of newer scripting languages like Python, Perl, and Ruby, shell scripting remains essential for system administration, application deployment, data processing pipelines, and development workflow automation.

The term "shell" refers to the command-line interface that wraps the operating system kernel, providing users and programs with a way to interact with system resources. Common shells include Bash (Bourne Again Shell), Zsh (Z Shell), Fish (Friendly Interactive Shell), and sh (Bourne Shell). Bash is the most widely deployed and is the default on most Linux distributions and macOS.

## Key Concepts

**Shebang (`#!`)** is the first line of a shell script that tells the operating system which interpreter to use to execute the script. For Bash scripts, this is typically `#!/bin/bash`. For more portable scripts, `#!/usr/bin/env bash` searches for bash in the PATH.

**Variables** store data for later use. Unlike compiled languages, shell variables are untyped by default. Variable assignment uses `=` without spaces: `name="value"`. Accessing variables requires a `$` prefix: `echo $name`.

**Positional Parameters** allow scripts to accept command-line arguments. `$0` is the script name, `$1` through `$9` are arguments, `$@` represents all arguments, and `$#` is the argument count.

**Control Structures** include conditionals (`if/then/else`, `case`), loops (`for`, `while`, `until`), and case statements for multi-way branching.

**Functions** enable code reuse and organization. Functions can accept parameters and return exit codes (not values).

**Exit Codes** indicate command success or failure. By convention, `0` means success, non-zero means failure. Scripts can check `$?` after commands or use `set -e` to exit on errors.

## How It Works

When a shell script executes, the shell interpreter reads the file line by line, parsing and executing each command in sequence. This process involves:

1. **Parsing** - The shell reads each line and breaks it into tokens (commands, arguments, operators)
2. **Expansion** - Variables (`$VAR`), command substitution (`` `cmd` `` or `$(cmd)`), and glob patterns (`*.txt`) are expanded
3. **Redirection** - Input/output redirection (`>`, `<`, `|`) is set up before command execution
4. **Execution** - The command is found (PATH lookup or absolute path) and run as a child process
5. **Wait/Collect** - The shell waits for the command to complete and collects its exit status

```bash
#!/bin/bash
# Example shell script demonstrating key features

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Variable assignment
GLOBAL_VAR="I am global"
readonly CONSTANT="cannot be modified"

# Function with local variables and arguments
process_files() {
    local input_dir="$1"
    local output_dir="$2"
    
    echo "Processing files from $input_dir to $output_dir"
    
    # Loop through files
    for file in "$input_dir"/*.txt; do
        if [[ -f "$file" ]]; then
            local basename=$(basename "$file")
            local output_path="$output_dir/$basename"
            
            # Process with error handling
            if grep -q "ERROR" "$file"; then
                echo "Skipping $file - contains errors" >&2
                return 1
            fi
            
            cat "$file" > "$output_path"
            echo "Processed: $basename"
        fi
    done
    
    return 0
}

# Main execution
main() {
    if [[ $# -ne 2 ]]; then
        echo "Usage: $0 <input_dir> <output_dir>" >&2
        return 1
    fi
    
    local input="$1"
    local output="$2"
    
    # Create output directory if it doesn't exist
    mkdir -p "$output"
    
    process_files "$input" "$output"
}

main "$@"
```

## Practical Applications

Shell scripting excels at system administration, file manipulation, and pipeline orchestration:

**System Administration** - Automating user management, backups, log rotation, service monitoring, and configuration management. Many Linux services use shell scripts for init scripts, cron jobs, and deployment hooks.

**Application Deployment** - Deployment scripts often use shell for orchestrating multi-step processes: building artifacts, stopping services, copying files, running migrations, and restarting services.

**Data Pipelines** - Processing logs, filtering data, converting formats, and chaining tools like `grep`, `sed`, `awk`, and `sort` into powerful data transformation pipelines.

**Development Workflows** - Automating builds, running test suites, managing git operations, scaffolding projects, and development environment setup.

**Text Processing** - Shell pipelines are exceptionally powerful for text manipulation: searching with `grep`, transforming with `sed` and `awk`, sorting with `sort`, and deduplicating with `uniq`.

## Examples

**Find and process large log files:**
```bash
#!/bin/bash
find /var/log -name "*.log" -size +100M | while read -r file; do
    echo "Compressing $file ($(du -h "$file" | cut -f1))"
    gzip "$file"
done
```

**Check service health and alert:**
```bash
#!/bin/bash
SERVICE="nginx"
HOST="localhost"
PORT=80

if ! nc -z "$HOST" "$PORT"; then
    echo "$(date): $SERVICE is DOWN on $HOST:$PORT" | \
        mail -s "Alert: $SERVICE down" admin@example.com
    exit 1
fi
echo "$(date): $SERVICE is UP"
```

**Parse CSV and generate summary:**
```bash
#!/bin/bash
awk -F',' '{
    total[$1] += $3;
    count[$1]++;
} END {
    for (dept in total) {
        avg = total[dept] / count[dept];
        printf "%s: total=%d, count=%d, avg=%.2f\n", dept, total[dept], count[dept], avg;
    }
}' data.csv | sort
```

## Related Concepts

- [[Bash]] - The most common Unix shell, often used interchangeably with shell scripting
- [[Linux]] - The operating system where shell scripting is most prevalent
- [[Command Line]] - The text-based interface shell scripts automate
- [[Cron]] - Time-based job scheduler often combined with shell scripts
- [[Sed]] - Stream editor for text transformation
- [[Awk]] - Pattern scanning and processing language
- [[Regular Expressions]] - Pattern matching used extensively in shell scripts

## Further Reading

- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [ShellCheck](https://www.shellcheck.net/) - Static analysis tool for shell scripts

## Personal Notes

Shell scripting's power lies in composing Unix utilities into pipelines. Learn to think in terms of text streams and filters. The `find | xargs` pattern is essential, as is understanding of exit codes and error handling. Always use `set -euo pipefail` in scripts that matter—it prevents silent failures. When a script exceeds a few hundred lines, consider whether Python or another language would be more maintainable. Shell is excellent for gluing together programs, not for complex business logic.
